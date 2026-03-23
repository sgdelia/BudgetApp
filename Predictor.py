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
    thresholds = pd.Series([0, 20, 50, 100, 500, int(10**6)])
   
    # convert categories to values
    CategoryClassifiers = df['Category'].unique()
    CategoryClassifiers = np.append(CategoryClassifiers, None)
    CategoryClassifiers = pd.Series(CategoryClassifiers)
    # convert description to values
    DescriptionClassifiers = df['Description'].unique()
    DescriptionClassifiers = np.append(DescriptionClassifiers, None)
    DescriptionClassifiers = pd.Series(DescriptionClassifiers)
    
    df['Amount'] = pd.cut(df['Amount'], bins=thresholds, labels=AmountClassifiers[:-1], right=False)
    df['Category'] = pd.Categorical(df['Category'], categories=CategoryClassifiers[:-1])
    df['Description'] = pd.Categorical(df['Description'], categories=DescriptionClassifiers[:-1])
    return df, thresholds, AmountClassifiers, CategoryClassifiers, DescriptionClassifiers
    
def predict(args=None, filePath=None):
    # predict category based on amount and description
    # print("This is the predictor file. It will be used to categorize expenses based on location and amount spent.")
    if args is None and filePath is not None:
        args = argparse.Namespace(filepath=filePath)
    else:
        parser = argparse.ArgumentParser(description='Process the budget file.')
        parser.add_argument('--filepath', type=str, help='the path to the budget file', default=filePath)
        args = parser.parse_args()
    try:
        if args.filepath is None:
            raise ValueError("File path is required. Please provide a valid file path using the --filepath argument.")
        fileName = args.filepath
        workingData = importAndClean(fileName)
        return workingData
    except Exception as e:
        print(f"An error occurred: {e}")
   
    

def main():
    predict(args=sys.argv[2:])

if __name__=="__main__":
    PredictorPath = str(pathlib.Path().resolve().parents[0] / "src")
    if PredictorPath not in sys.path:
        sys.path.insert(0, PredictorPath)
    main()