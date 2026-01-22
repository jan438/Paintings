import drawsvg as draw
import math
import sys
import os
import csv
from PIL import Image, ImageOps, ImageDraw
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch, mm
from reportlab.lib.pagesizes import portrait, landscape, A4
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import red, yellow, green
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg, load_svg_file, SvgRenderer
from pypdf import PdfReader, PdfWriter

def processreport():
    merger = PdfWriter()
    for i in range(3):
        strindex = "{:03d}".format(i)
        print(strindex)
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
#    for i in range(3):
#        strindex = "{:03d}".format(i)
#        if os.path.isfile("PDF/100paintings" + str(strindex) + ".pdf"):
#            os.remove("PDF/100paintings" + str(strindex) + ".pdf")

if sys.platform[0] == 'l':
    path = '/home/jan/git/Paintings'
if sys.platform[0] == 'w':
    path = "C:/Users/janbo/OneDrive/Documents/GitHub/Paintings"
os.chdir(path)
processreport()
key = input("Wait")
