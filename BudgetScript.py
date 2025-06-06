import pandas as pd
import numpy as np

def importAndClean(fileName):
    cleaned = pd.read_excel(fileName, header=6)
    print(cleaned.head())   
    #get Date, Amount, Description, and "In Spreadsheet" columns

    headers = ["Date", "Amount", "Description", "In Spreadsheet"]
    workingData = pd.DataFrame({})
    for header in headers:
        extractedCol = cleaned[header]
        workingData[header] = extractedCol #pd.concat([extractedCol, workingData])
    print(workingData.head())
    return workingData
      
def categorize(workingData):
    # filler function until UI for categorizing is made
    if "Category" in workingData:
        return workingData
    #doesn't exist, fill with NaN
    workingData["Category"] = np.nan
    return workingData

def main():
    workingData = importAndClean("C:\\Users\\sophi\\Downloads\\activity.xlsx")
    categorize(workingData)
    print(workingData.head())

# Anything below here is considered "main"
main()