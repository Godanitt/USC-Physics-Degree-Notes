# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 13:49:10 2024

@author: danie
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer

# Crear un archivo PDF
pdf_filename = "standard_model_replica.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=A4)

# Estilos de texto
styles = getSampleStyleSheet()
title_style = styles["Title"]
body_style = styles["BodyText"]

# Contenido del PDF
content = []

# Título
title = Paragraph("Standard Model of Elementary Particles", title_style)
content.append(title)
content.append(Spacer(1, 12))

# Datos de la tabla
data = [
    ["QUARKS", "", "", ""],
    ["Up", "u", "2.16 MeV/c²", "+2/3"],
    ["Charm", "c", "1.27 GeV/c²", "+2/3"],
    ["Top", "t", "173 GeV/c²", "+2/3"],
    ["Down", "d", "4.7 MeV/c²", "-1/3"],
    ["Strange", "s", "96 MeV/c²", "-1/3"],
    ["Bottom", "b", "4.18 GeV/c²", "-1/3"],
    ["", "", "", ""],  # Espacio en blanco
    ["LEPTONS", "", "", ""],
    ["Electron", "e", "0.511 MeV/c²", "-1"],
    ["Muon", "μ", "105.7 MeV/c²", "-1"],
    ["Tau", "τ", "1777 MeV/c²", "-1"],
    ["Electron Neutrino", "νₑ", "< 2.2 eV/c²", "0"],
    ["Muon Neutrino", "νμ", "< 0.17 MeV/c²", "0"],
    ["Tau Neutrino", "ντ", "< 15.5 MeV/c²", "0"],
    ["", "", "", ""],  # Espacio en blanco
    ["BOSONS", "", "", ""],
    ["Photon", "γ", "0", "0"],
    ["W Boson", "W", "80.38 GeV/c²", "±1"],
    ["Z Boson", "Z", "91.19 GeV/c²", "0"],
    ["Gluon", "g", "0", "0"],
    ["Higgs Boson", "H", "125.1 GeV/c²", "0"],
]

# Crear la tabla
table = Table(data, colWidths=[120, 60, 100, 60])
table.setStyle(TableStyle([
    # Estilo para los encabezados de sección
    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
    ("BACKGROUND", (0, 8), (-1, 8), colors.grey),
    ("BACKGROUND", (0, 16), (-1, 16), colors.grey),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
    ("TEXTCOLOR", (0, 8), (-1, 8), colors.whitesmoke),
    ("TEXTCOLOR", (0, 16), (-1, 16), colors.whitesmoke),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTNAME", (0, 8), (-1, 8), "Helvetica-Bold"),
    ("FONTNAME", (0, 16), (-1, 16), "Helvetica-Bold"),
    # Estilo para las filas de datos
    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
    ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
]))

content.append(table)

# Generar el PDF
doc.build(content)

print(f"PDF generado: {pdf_filename}")