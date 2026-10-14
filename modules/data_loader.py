import pandas as pd

def load_data(file):

    xls = pd.ExcelFile(file)

    sheets = {}

    for sheet in xls.sheet_names:
        sheets[sheet] = pd.read_excel(
            file,
            sheet_name=sheet
        )

    return sheets
