from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph
)

from reportlab.lib.styles import getSampleStyleSheet

def export_pdf(commentaire):

    filename = "Rapport_FCP.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = [
        Paragraph(
            commentaire,
            styles["Normal"]
        )
    ]

    doc.build(story)

    return filename
