import pandas as pd
import pathlib
import argparse

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

def CategoryCleaning(workingData):
    # convert description to values
    # convert date to values
    df: pd.DataFrame = workingData.copy()
    # convert categories to values
    categories: list[str] = []
    for cat in df['Category']:
        category = str.upper(cat).strip()[:5]
        categories.append(category)
    df['Category'] = pd.DataFrame(categories)
    return df

def DescCleaning(workingData):
    df:pd.DataFrame = workingData.copy()
    descriptions: list[str] = []
    for desc in df['Description']:
        descrip = str.upper(desc).strip()[:10]
        descriptions.append(descrip)
    df['Description'] = pd.DataFrame(descriptions)
    return df
    
    
def Clean(filePath=None) -> pd.DataFrame:
    # predict category based on amount and description
    # print("This is the predictor file. It will be used to categorize expenses based on location and amount spent.")
    if filePath == None:
        print("File path required. Exiting.")
        quit
    workingData = importAndClean(filePath)
    cleanCats: pd.DataFrame = CategoryCleaning(workingData=workingData)
    cleanDescs: pd.DataFrame = DescCleaning(workingData=workingData)
    outData: pd.DataFrame = workingData.copy()
    outData['Description'] = cleanDescs['Description']
    outData['Category'] = cleanCats['Category']
    return outData
   
    
def main():
    parser = argparse.ArgumentParser(description='Process the budget file.')
    parser.add_argument('--filepath', type=str, help='the path to the budget file', required=True)
    args = parser.parse_args()
    Clean(args.filepath)

if __name__=="__main__":
    main()
    
    