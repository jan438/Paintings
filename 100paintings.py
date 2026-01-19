import drawsvg as draw
import math
import sys
import os
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch, mm

paintingsdata = []

if sys.platform[0] == 'l':
    path = '/home/jan/git/Paintings'
if sys.platform[0] == 'w':
    path = "C:/Users/janbo/OneDrive/Documents/GitHub/Paintings"
os.chdir(path)

file_to_open = "Data/100paintings.csv"
with open(file_to_open, 'r') as file:
    csvreader = csv.reader(file, delimiter = ';')
    count = 0
    for row in csvreader:
        paintingsdata.append(row)
        count += 1
print(count)
c = canvas.Canvas("PDF/100paintings.pdf")
c.setFillColor(HexColor('#FECDE5'))
c.save()
key = input("Wait")
