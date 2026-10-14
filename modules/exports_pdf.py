from fpdf import FPDF

def create_pdf(commentary):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font(
        "Arial",
        size=12
    )

    pdf.multi_cell(
        0,
        8,
        commentary
    )

    return pdf.output(
        dest="S"
    )
