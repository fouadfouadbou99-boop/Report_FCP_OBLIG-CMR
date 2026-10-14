import pandas as pd


def load_data(uploaded_file):

    # DATA PERF

    perf_raw = pd.read_excel(
        uploaded_file,
        sheet_name="Data Perf",
        header=None
    )

    # Historique VL

    perf_df = pd.DataFrame()

    perf_df["Date"] = perf_raw.iloc[63:105, 1].values

    perf_df["SANADATE_VL"] = perf_raw.iloc[63:105, 2].values

    perf_df["SANADATE_PERF_W"] = perf_raw.iloc[63:105, 3].values

    perf_df["SANADATE_YTD"] = perf_raw.iloc[63:105, 4].values

    perf_df["BONDS_VL"] = perf_raw.iloc[63:105, 5].values

    perf_df["BONDS_PERF_W"] = perf_raw.iloc[63:105, 6].values

    perf_df["BONDS_YTD"] = perf_raw.iloc[63:105, 7].values

    perf_df["OBLIG_VL"] = perf_raw.iloc[63:105, 8].values

    perf_df["OBLIG_PERF_W"] = perf_raw.iloc[63:105, 9].values

    perf_df["OBLIG_YTD"] = perf_raw.iloc[63:105, 10].values

    perf_df = perf_df.dropna()

    # SENSIBILITES

    sens_raw = pd.read_excel(
        uploaded_file,
        sheet_name="Data Sensibilité"
    )

    sens_df = sens_raw.copy()

    return perf_df, sens_df
