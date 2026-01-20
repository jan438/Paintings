import drawsvg as draw
import math
import sys
import os
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch, mm
from reportlab.lib.pagesizes import landscape, A4

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
width, height = A4
c = canvas.Canvas("PDF/100paintings.pdf", (landscape(A4)))
c.setFillColor(HexColor('#FECDE5'))
for i in range(count):
    if i == 3:
        break
    c.drawString(10, 200 - i * 30, paintingsdata[i][0])
c.save()
key = input("Wait")
