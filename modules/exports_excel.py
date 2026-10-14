from io import BytesIO
import pandas as pd


def export_excel(
        perf_metrics,
        risk_metrics):

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        perf_metrics.to_excel(
            writer,
            sheet_name="Performance",
            index=False
        )

        risk_metrics.to_excel(
            writer,
            sheet_name="Risque",
            index=False
        )

    return output.getvalue()
