import drawsvg as draw
import math
import sys
import os
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch, mm
from reportlab.lib.pagesizes import portrait, landscape, A4
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import red, yellow, green
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg, load_svg_file, SvgRenderer
from pypdf import PdfReader, PdfWriter
from reportlab.platypus import Image

maxpaintings = 28
paintingsdata = []
infoyline = 150

def processreport():
    merger = PdfWriter()
    for i in range(maxpaintings):
        strindex = "{:03d}".format(i)
        #print(strindex)
        if os.path.isfile("PDF/100paintings" + str(strindex) + ".pdf"):
            inputpdf = open("PDF/100paintings" + str(strindex) + ".pdf", "rb")
            merger.append(inputpdf)
            inputpdf.close()
        else:
            break
    output = open("PDF/Total.pdf", "wb")
    merger.write(output)
    merger.close()
    output.close()
#    for i in range(maxpaintings):
#        strindex = "{:03d}".format(i)
#        if os.path.isfile("PDF/100paintings" + str(strindex) + ".pdf"):
#            os.remove("PDF/100paintings" + str(strindex) + ".pdf")

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
for i in range(maxpaintings):
    painting = "Paintings/" + paintingsdata[i][0] + ".jpg"
    I = Image(painting)
    w = I.drawWidth
    h = I.drawHeight
    # 841.89
    # 595.27
    # nightwatch = 2.5?
    if h >= 0.75 * w:
        mode = "P"
        minmarginhor = 60
        minmarginver = 60
        roomhor = 595.27 - 2 * minmarginhor
        roomver = 841.89 - infoyline - 2 * minmarginver
        schor = roomhor / w
        scver = roomver / h
        sc = min(schor, scver)
    else:
        mode = "L"
        minmarginhor = 60
        minmarginver = 60
        roomhor = 841.89 - 2 * minmarginhor
        roomver = 595.27 - infoyline - 2 * minmarginver
        schor = w / roomhor
        scver = h / roomver
        sc = min(schor, scver)
    print(i, paintingsdata[i][0], "W", w, "H", h, "Room", round(roomhor, 3), round(roomver, 3), "Sc", round(schor, 3), round(scver, 3),"mode", mode)
processreport()
key = input("Wait")
