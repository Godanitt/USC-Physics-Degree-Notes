# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 13:49:10 2024

@author: danie
"""

import lattpy as lp
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer

# Crear un archivo PDF
pdf_filename = "standard_model.pdf"
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

# Tabla de partículas
data = [
    ["Type", "Particle", "Symbol", "Mass", "Charge", "Spin"],
    ["Quarks", "Up", "u", "2.16 MeV/c²", "+2/3", "1/2"],
    ["", "Charm", "c", "1.27 GeV/c²", "+2/3", "1/2"],
    ["", "Top", "t", "173 GeV/c²", "+2/3", "1/2"],
    ["", "Down", "d", "4.7 MeV/c²", "-1/3", "1/2"],
    ["", "Strange", "s", "96 MeV/c²", "-1/3", "1/2"],
    ["", "Bottom", "b", "4.18 GeV/c²", "-1/3", "1/2"],
    ["Leptons", "Electron", "e", "0.511 MeV/c²", "-1", "1/2"],
    ["", "Muon", "μ", "105.7 MeV/c²", "-1", "1/2"],
    ["", "Tau", "τ", "1777 MeV/c²", "-1", "1/2"],
    ["", "Electron Neutrino", "νₑ", "< 2.2 eV/c²", "0", "1/2"],
    ["", "Muon Neutrino", "νμ", "< 0.17 MeV/c²", "0", "1/2"],
    ["", "Tau Neutrino", "ντ", "< 15.5 MeV/c²", "0", "1/2"],
    ["Bosons", "Photon", "γ", "0", "0", "1"],
    ["", "W Boson", "W", "80.38 GeV/c²", "±1", "1"],
    ["", "Z Boson", "Z", "91.19 GeV/c²", "0", "1"],
    ["", "Gluon", "g", "0", "0", "1"],
    ["", "Higgs Boson", "H", "125.1 GeV/c²", "0", "0"],
]

# Crear la tabla
table = Table(data)
table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
    ("GRID", (0, 0), (-1, -1), 1, colors.black),
]))

content.append(table)

# Generar el PDF
doc.build(content)

print(f"PDF generado: {pdf_filename}")