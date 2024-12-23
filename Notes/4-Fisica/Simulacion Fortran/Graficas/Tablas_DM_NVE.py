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

dfp1=df.iloc[:3]
dfp2=df.iloc[3:11]
dfp3=df.iloc[11:]

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
latex_table1 = dfp1.to_latex(index=False,float_format="%.4f")
latex_table2 = dfp2.to_latex(index=False,float_format="%.4f")
latex_table3 = dfp3.to_latex(index=False,float_format="%.4f")
latex_table4 = df2.to_latex(index=False,float_format="%.4f")


# Imprimir la tabla en formato LaTeX

archivotex1 = os.path.join('..', 'Memorias','Ejercicio-3_Memoria','Tabla1.tex')
archivotex2 = os.path.join('..', 'Memorias','Ejercicio-3_Memoria','Tabla2.tex')
archivotex3 = os.path.join('..', 'Memorias','Ejercicio-3_Memoria','Tabla3.tex')
archivotex4 = os.path.join('..', 'Memorias','Ejercicio-3_Memoria','Tabla4.tex')

with open(archivotex1, 'w') as f:
    f.write(latex_table1)
    
with open(archivotex2, 'w') as f:
    f.write(latex_table2)
    
with open(archivotex3, 'w') as f:
    f.write(latex_table3)
    
with open(archivotex4, 'w') as f:
    f.write(latex_table4)
    
    
    