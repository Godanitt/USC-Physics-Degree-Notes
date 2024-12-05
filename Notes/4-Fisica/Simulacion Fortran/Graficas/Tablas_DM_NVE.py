# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 00:02:09 2024

@author: danie
"""

import pandas as pd

import os 

# Leer el archivo .dat usando pandas
archivox = os.path.join('..', 'Datos','Obligatorio3','Datos_DM_NVE_medias.dat')
archivox2 = os.path.join('..', 'Datos','Obligatorio3','Datos_DM_NVE.dat')
df = pd.read_csv(archivox, delim_whitespace=True, header=None, 
                 names=['Variable', 'Media', 'Incertidumbre'])

df2 = pd.read_csv(archivox2,delim_whitespace=True, header=None,
         names=["$E_c^*$", "$E_p^*$", "$E_t^*$", "$T^*$", "$P^*$",
            "$C_V^*$", "$\\alpha_E^*$", "$\gamma^*$","$1/k_s^*$"])

#"$E_c^*$" & "$E_p^*$" & "$E_t^*$" & "$T^*$" & "$P^*$" & "$C_V^*$"
# & "$\alpha_E^*$" & "$\gamma^*$" & "$1/k_s^*$"

# Mostrar el DataFrame (opcional, para ver los datos)
#print(df)
"""
styler=df.style
styler.to_latex(
    column_format="cc|cc",
    position="h!",
    caption="Tabla de datos con media e incertidumbre", 
    label="tab:datos",
    clines="skip-last;data",
    siunitx="True",
    convert_css=True,
    position_float="centering",
    multicol_align="|c|",
    hrules=True)
styler=df2.style
styler.to_latex(
        column_format="cc|cc",
        position="h!",
        caption="Tabla de datos con media e incertidumbre", 
        label="tab:datos",
        clines="skip-last;data",
        siunitx="True",
        convert_css=True,
        position_float="centering",
        multicol_align="|c|",
        hrules=True)

"""
# Convertir a formato LaTeX
latex_table = df.to_latex(index=False,float_format="%.4f")
excel_table= df2.to_csv()
latex_table2 = df2.to_latex(index=False,float_format="%.4f")

# Imprimir la tabla en formato LaTeX
print(latex_table)
print(latex_table2)

archivotex = os.path.join('..', 'Memorias','Ejercicio-3_Memoria','Tabla1.tex')
archivotex2 = os.path.join('..', 'Memorias','Ejercicio-3_Memoria','Tabla2.tex')
archivoexcel = os.path.join('..', 'Memorias','Ejercicio-3_Memoria','Tabla2.csv')

with open(archivotex, 'w') as f:
    f.write(latex_table)
with open(archivotex2, 'w') as f:
    f.write(latex_table2)
with open(archivoexcel, 'w') as f:
    f.write(excel_table)