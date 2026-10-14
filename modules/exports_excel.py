from openpyxl import Workbook

def export_excel(df):

    wb = Workbook()

    ws = wb.active

    ws.title = "KPIs"

    filename = "Rapport_FCP.xlsx"

    wb.save(filename)

    return filename
