import pandas as pd
import numpy as np
import sklearn as sk
import sys
import pathlib

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

def main():
    print("This is the predictor file. It will be used to categorize expenses based on location and amount spent.")
    fileName = input("Enter the name of the file you want to use: ")
    workingData = importAndClean(fileName)
    print(workingData)

if __name__=="__main__":
    main()