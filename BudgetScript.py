import pandas as pd
import numpy as np
import sys
from PySide6.QtWidgets import QApplication, QLabel
from pathlib import Path

def importAndClean(fileName):
    properFormat = fileName.replace('"','').replace('"', '')
    properFormat = Path(properFormat)
    cleaned = pd.read_excel(properFormat, sheet_name="Cleaned Data", header=0)
    print(cleaned.head())   
    #get Date, Amount, Description, and "In Spreadsheet" columns

    # Prompt for option to include "Category"?
    # headers = ["Date", "Amount", "Description", "In Spreadsheet", "Category"]
    headers = ["Date", "Amount", "Description", "Category"]

    workingData = pd.DataFrame({})
    for header in headers:
        extractedCol = cleaned[header]
        workingData[header] = extractedCol
    return workingData
      
def categorize(workingData):
    # no vals, make them
    if "Category" not in workingData:
        workingData["Category"] = np.nan
        # add category entry here
    #sum by category
    sumEachCategory = workingData.groupby("Category")["Amount"].sum()
    print(sumEachCategory)

def excelFormatting(workingData):   
    sorted = workingData.groupby("Category")
    formsAndGroups = list()
    sortedList = list(sorted)
    for group in sortedList:
        formula = "="
        for value in list(group[1]["Amount"]):
            formula = formula + str(value) + "+"
        formula = formula.removesuffix("+") 
        dictOfVals = dict(Formula=formula, Category=group[0])  
        formsAndGroups.append(dictOfVals)
    pd.DataFrame(formsAndGroups).to_clipboard()
    print("Excel formulas copied to clipboard")
    


# def uiTest():
#     app = QApplication(sys.argv)
#     label = QLabel("Hello World!")
#     label.show()
#     app.exec()

def main():
    filepath = input("Enter the path to the budget file: ")
    workingData = importAndClean(filepath)
    print(workingData)
    categorize(workingData)
    excelFormatting(workingData)
    # uiTest()

if __name__=="__main__":
    main()