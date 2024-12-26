# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 18:26:20 2024

@author: danie
"""
from ase.build import bulk
from ase.visualize import view

# Create an FCC lattice for Aluminum
fcc_lattice = bulk('Al', crystalstructure='fcc', a=4.05, cubic=True)

# Visualize the lattice
view(fcc_lattice)

# Save the lattice structure to a CIF file
fcc_lattice.write("fcc_lattice.cif")