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

    perf.columns = [
        "Date",
        "SANADATE_VL",
        "SANADATE_PERF_W",
        "SANADATE_YTD",
        "BONDS_VL",
        "BONDS_PERF_W",
        "BONDS_YTD",
        "OBLIG_VL",
        "OBLIG_PERF_W",
        "OBLIG_YTD",
        "MBI_MT",
        "BENCH_PERF",
        "BENCH_SPREAD",
        "VOL_BENCH"
    ]

    perf["Date"] = pd.to_datetime(
        perf["Date"],
        errors="coerce"
    )

    perf = perf.dropna(subset=["Date"])

    return perf, sensi
