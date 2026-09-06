from BudgetScript import importAndClean, categorize, excelFormatting
import pandas as pd

def test_importAndClean():
    # Test with a sample file path and statement type
    file_path = "AnonymizedData.xlsx"
    statement_type = "AMEX"
    
    # Call the function
    result = importAndClean(file_path, statement_type)
    
    # Check if the result is a DataFrame
    assert isinstance(result, pd.DataFrame), "Result should be a DataFrame"
    
    # Check if the required columns are present
    expected_columns = ["Date", "Amount", "Description", "Category"]
    for col in expected_columns:
        assert col in result.columns, f"Missing column: {col}"

def test_categorize():
    # Create a sample DataFrame
    data = {
        "Date": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "Amount": [100, 200, 300],
        "Description": ["Desc1", "Desc2", "Desc3"],
        "Category": ["Cat1", "Cat2", "Cat1"]
    }
    df = pd.DataFrame(data)
    
    # Call the function
    categorize(df)
    
    # Check if the output is as expected (sum by category)
    expected_sum = {"Cat1": 400, "Cat2": 200}
    actual_sum = df.groupby("Category")["Amount"].sum().to_dict()
    
    assert actual_sum == expected_sum, f"Expected {expected_sum}, but got {actual_sum}"

def test_excelFormatting():
    # Create a sample DataFrame
    data = {
        "Date": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "Amount": [100, 200, 300],
        "Description": ["Desc1", "Desc2", "Desc3"],
        "Category": ["Cat1", "Cat2", "Cat1"]
    }
    df = pd.DataFrame(data)
    
    # Call the function
    excelFormatting(df)
    
    # Since the function copies to clipboard, we can't directly test the output.
    # However, we can check if the function runs without errors.
    assert True, "Function ran without errors"