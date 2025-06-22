import pandas as pd
import numpy as np
import sys
from PySide6.QtWidgets import QApplication, QLabel

def importAndClean(fileName):
    cleaned = pd.read_excel(fileName, header=6)
    print(cleaned.head())   
    #get Date, Amount, Description, and "In Spreadsheet" columns

    # Prompt for option to include "Category"?
    headers = ["Date", "Amount", "Description", "In Spreadsheet", "Category"]
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


# def uiTest():
#     app = QApplication(sys.argv)
#     label = QLabel("Hello World!")
#     label.show()
#     app.exec()

def main():
    workingData = importAndClean("C:\\Users\\sophi\\Downloads\\activity.xlsx")
    print(workingData)
    categorize(workingData)
    # uiTest()

if __name__=="__main__":
    main()