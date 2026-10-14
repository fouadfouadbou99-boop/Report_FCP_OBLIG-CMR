import pandas as pd

def load_data(file):

    perf = pd.read_excel(
        file,
        sheet_name="Data Perf"
    )

    sensi = pd.read_excel(
        file,
        sheet_name="Data Sensibilité"
    )

    return perf, sensi
