import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sklearn as sk
from sklearn.linear_model import LinearRegression
import sys
import pathlib
import argparse
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog

def importAndClean(fileName):
    properFormat = fileName.replace('"','').replace('"', '')
    properFormat = pathlib.Path(properFormat)
    cleaned = pd.read_excel(properFormat, sheet_name=0, header=0, engine='openpyxl')
    # print(cleaned.head())   
    #get Date, Amount, Description, and "Category" columns

    headers = ["Date", "Amount", "Description", "Category"]

    workingData = pd.DataFrame({})
    for header in headers:
        extractedCol = cleaned[header]
        workingData[header] = extractedCol
    return workingData

def ConvertToValues(workingData):
    # convert description to values
    # convert date to values
    df = workingData.copy()
    AmountClassifiers = pd.Series(["Very Low", "Low", "Medium", "High", "Very High", None])
    # convert categories to values
    categories: list[str] = []
    for cat in df['Category']:
        category = str.upper(cat).strip()
        categories.append(category)
        df = df.replace(cat,category)
    np.append(categories, None)
    CategoryClassifiers = pd.Series(categories).unique()
    # convert description to values
    DescriptionClassifiers = df['Description'].unique()
    DescriptionClassifiers = np.append(DescriptionClassifiers, None)
    
    df['Amount'] = pd.cut(df['Amount'], bins=CategoryClassifiers.size)
    
    return df, AmountClassifiers, CategoryClassifiers, DescriptionClassifiers
    
def predict(filePath=None):
    # predict category based on amount and description
    # print("This is the predictor file. It will be used to categorize expenses based on location and amount spent.")
    if filePath == None:
        print("File path required. Exiting.")
        quit
    workingData = importAndClean(filePath)
    outData = ConvertToValues(workingData=workingData)
    return outData
   
    
def main():
    parser = argparse.ArgumentParser(description='Process the budget file.')
    parser.add_argument('--filepath', type=str, help='the path to the budget file', required=True)
    args = parser.parse_args()
    predict(args.filepath)

if __name__=="__main__":
    main()