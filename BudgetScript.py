import pandas as pd
import numpy as np
import sys
import argparse

from pathlib import Path

def importAndClean(fileName, typeOfStatment: str = 'other'):
    properFormat = fileName.replace('"','').replace('"', '')
    properFormat = Path(properFormat)

    if typeOfStatment.upper() == 'AMEX':
        cleaned = pd.read_excel(properFormat, sheet_name=0, header=6)
    elif typeOfStatment.upper() == 'BANK':
        cleaned = pd.read_csv(properFormat)
        colsToDrop = ['Bank RTN', 'Account Number', 'Transaction Type', 'Check Number',]
        cleaned = cleaned.drop(colsToDrop, axis=1)
        CredsAndDebs = cleaned['Debit'].to_frame()
        CredsAndDebs = CredsAndDebs.join(cleaned['Credit'].to_frame())
        Total = CredsAndDebs['Debit'].sum() - CredsAndDebs['Credit'].sum()
        cleaned.insert(1,'Amount', Total)
        try:
            index: int = cleaned.columns.names.count('Category')
        except:
            cleaned.insert(3,column='Category', value="")
        cleaned = cleaned.drop(['Credit', 'Debit'], axis=1)
    else:
        cleaned = pd.read_excel(properFormat, sheet_name=0, header=0)
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
    framed = pd.DataFrame(formsAndGroups)
    framed.to_clipboard(index=False, header=False)
    print("Excel formulas copied to clipboard")
    

def main():
    parser = argparse.ArgumentParser(prog='Budget Script', description='Parses Excel spreadsheets of spending data, consolidates, and creates budget formulas')
    parser.add_argument('-p', '--path', type=str, help='Path to expense export (excel files only)', required=True)
    parser.add_argument('-t', '--type', type=str, required=True, help="Type of statement: amex, bank, or other")
    args = parser.parse_args()
    filepath = args.path
    typeOfStatement: str = args.type
    workingData = importAndClean(filepath, typeOfStatement)
    print(workingData)
    categorize(workingData)
    excelFormatting(workingData)
    # uiTest()

if __name__=="__main__":
    main()