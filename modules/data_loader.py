import pandas as pd


def load_data(uploaded_file):

    perf_raw = pd.read_excel(
        uploaded_file,
        sheet_name="Data Perf",
        header=None
    )

    perf_df = pd.DataFrame()

    perf_df["Date"] = perf_raw.iloc[63:105, 1].values

    perf_df["SANADATE_VL"] = pd.to_numeric(
        perf_raw.iloc[63:105, 2],
        errors="coerce"
    )

    perf_df["BONDS_VL"] = pd.to_numeric(
        perf_raw.iloc[63:105, 5],
        errors="coerce"
    )

    perf_df["OBLIG_VL"] = pd.to_numeric(
        perf_raw.iloc[63:105, 8],
        errors="coerce"
    )

    perf_df = perf_df.dropna()

    perf_df.reset_index(
        drop=True,
        inplace=True
    )

    sens_df = pd.read_excel(
        uploaded_file,
        sheet_name="Data Sensibilité"
    )

    return perf_df, sens_df
