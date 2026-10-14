from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)


def export_pdf(commentaire):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer
    )

    styles = getSampleStyleSheet()

    content = [

        Paragraph(
            "Rapport Comité",
            styles["Title"]
        ),

        Spacer(1,12),

        Paragraph(
            commentaire,
            styles["BodyText"]
        )

    ]

    doc.build(content)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf
