# BudgetApp
A Python project written to import and clean personal expense data from an Excel or csv export. Standardizes "Date," "Amount," "Description," and "Category" data. Total expenses are itemized, summed by category, and copied to clipboard. 
# Example Usage
## Arguments
- --filepath is the location of the exported data
- -t is the type of statement export, either 'bank' or 'amex'  

## Example
python3 BudgetScript.py --filepath <Path to Export\> -t <Export Type\>