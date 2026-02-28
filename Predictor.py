import pandas as pd
import numpy as np
import sklearn as sk
import sys
import pathlib
import argparse

def importAndClean(fileName):
    properFormat = fileName.replace('"','').replace('"', '')
    properFormat = pathlib.Path(properFormat)
    cleaned = pd.read_excel(properFormat, sheet_name=0, header=0)
    print(cleaned.head())   
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
    thresholds = pd.Series([0, 20, 50, 100, 500, np.inf])
    df['Amount'] = np.where(df['Amount'] <= thresholds[1], AmountClassifiers[0],
                    np.where(df['Amount'] <= thresholds[2], AmountClassifiers[1],
                    np.where(df['Amount'] <= thresholds[3], AmountClassifiers[2],
                    np.where(df['Amount'] <= thresholds[4], AmountClassifiers[3],
                    np.where(df['Amount'] <= thresholds[5], AmountClassifiers[4], AmountClassifiers[5])))))
   
    # convert categories to values
    CategoryClassifiers = df['Category'].unique()
    CategoryClassifiers = np.append(CategoryClassifiers, None)
    CategoryClassifiers = pd.Series(CategoryClassifiers)
    # convert description to values
    DescriptionClassifiers = df['Description'].unique()
    DescriptionClassifiers = np.append(DescriptionClassifiers, None)
    DescriptionClassifiers = pd.Series(DescriptionClassifiers)
    return df
    
    

def initializeModel(workingData):
    # initialize model here
    X = workingData[["Amount", "Description"]]
    y = workingData["Category"]
    r = sk.linear_model.LinearRegression()
    r.fit(X, y)
    return r

def main():
    print("This is the predictor file. It will be used to categorize expenses based on location and amount spent.")
    parser = argparse.ArgumentParser(description='Process the budget file.')
    parser.add_argument('--filepath', type=str, help='the path to the budget file')
    args = parser.parse_args()
    fileName = args.filepath
    workingData = importAndClean(fileName)
    processedData =ConvertToValues(workingData)
    print(processedData.head())

    # model = initializeModel(workingData)
    # print(model)

if __name__=="__main__":
    main()