from io import BytesIO

from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import inch, landscape, A4, cm
from django.shortcuts import render

from reportlab.platypus.doctemplate import SimpleDocTemplate
from reportlab.platypus import Paragraph

from reportlab.lib.styles import getSampleStyleSheet


def view1(request):
    return HttpResponse("Hola mundo Django!!!!")


def report(request):
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachement; filename=Archivo.pdf'

    # a = canvas.Canvas()
    # a.drawText("Hola mundo!")
    buffer = BytesIO()

    doc = SimpleDocTemplate("test_report_lab.pdf", pagesize=letter, rightMargin=40, leftMargin=40, topMargin=60,
                            bottomMargin=18)
    # doc.pagesize = landscape(A4)

    elements = []
    styles = getSampleStyleSheet()

    styles = styles["BodyText"]

    description = Paragraph("CENSOS NACIONALES 2017; XII DE POBLACIÓN, VII DE VIVIENDA Y III DE COMUNIDADES INDÉGENAS",
                            styles)
    subtitle = Paragraph("LISTADO DE VIVIENDAS DEL ÁREA DE EMPADRONAMIENTO URBANO (A.E.U.)", styles)

    headings = (
    'VIV Nº', 'MANZANA Nº', 'FRENTE Nº', 'DIRECCIÒN DE LA VIVIENDA', 'Apellidos y Nombres del JEFE DEL HOGAR')

    data = [
        ["(1)", "(2)", "(3)", "(4)", "(5)"],
        ["A", "01", "ABCD", "Anthony"],
        ["B", "02", "CDEF", "Brian"],
        ["C", "03", "SDFSDF", "Carlos"],
        ["D", "04", "SDFSDF", "Luis"],
        ["E", "05", "GHJGHJGHJ", "Farfan"],
    ]

    # TODO: Get this line right instead of just copying it from the docs

    alldatas = [[Paragraph(cell, styles) for cell in row] for row in data]

    t = Table([headings] + alldatas)
    t.setStyle(TableStyle(
        [
            ('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
            ('TEXTCOLOR', (1, 1), (-2, -2), colors.red),
            ('VALIGN', (0, 0), (0, -1), 'TOP'),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.blue),
            ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
            ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.green),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ]
    ))

    # style = getSampleStyleSheet()
    # t = styles["BodyText"]

    # t.wordWrap = 'CJK'

    # c.drawString(275, 725, 'AMOUNT OWED:')
    # c.drawString(500, 725, "$1,000.00")
    # c.line(378, 723, 580, 723)
    # c.drawString(30, 703, 'RECIBIDO DE:')
    # c.line(120, 700, 580, 700)
    # c.drawString(120, 703, "ANTHONY CARRILLO")
    elements.append(description)
    elements.append(subtitle)
    elements.append(t)
    doc.build(elements)
    # t.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
