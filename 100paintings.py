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
from reportlab.lib.colors import red, yellow, green, white, gold, brown
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg, load_svg_file, SvgRenderer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image

paintingsdata = []
paintingfont = "LiberationSerif"
#pagesize=(595.27, 841.89)
centerportrait = (297.635, 481.695)
centerlandscape = (420.945, 357.638)
infoyline = 120
#centeryportait 841.39 - 120 = 721.39 / 2 = 361.695 + 120 = 481.695
#centerylandscape 595.27 - 120 = 475.27 / 2 = 237.635 + 120 = 357.638

def scaleSVG(svgfile, scaling_factor):
    svg_root = load_svg_file(svgfile)
    svgRenderer = SvgRenderer(svgfile)
    drawing = svgRenderer.render(svg_root)
    scaling_x = scaling_factor
    scaling_y = scaling_factor
    drawing.width = drawing.minWidth() * scaling_x
    drawing.height = drawing.height * scaling_y
    drawing.scale(scaling_x, scaling_y)
    return drawing

def add_frame(c, mode, x, y, w, h,  color1, color2):
    if mode == "1":
        c.setLineCap(2)
        c.setStrokeColor(color2)
        c.setLineWidth(1)
        p = c.beginPath()
        p.moveTo(x, y)
        p.lineTo(x, y + h)
        p.lineTo(x + w, y + h)
        p.lineTo(x + w, y)
        p.lineTo(x, y)
        c.drawPath(p, fill = 0, stroke = 1)
        c.setStrokeColor(color1)
        c.setLineWidth(6)
        p = c.beginPath()
        p.moveTo(x - 3, y - 3)
        p.lineTo(x - 3, y + h + 3)
        p.lineTo(x + w + 3, y + h + 3)
        p.lineTo(x + w + 3, y - 3)
        p.lineTo(x - 3, y - 3)
        c.drawPath(p, fill = 0, stroke = 1)
    elif mode == "2":
        c.setLineCap(2)
        c.setStrokeColor(color2)
        c.setLineWidth(10)
        p = c.beginPath()
        p.moveTo(x - 12, y - 12)
        p.lineTo(x - 12, y + h + 12)
        p.lineTo(x + w + 12, y + h + 12)
        p.lineTo(x + w + 12, y + 12)
        p.lineTo(x - 12, y -12)
        c.drawPath(p, fill = 0, stroke = 1)
        c.setStrokeColor(color1)
        c.setLineWidth(6)
        p = c.beginPath()
        p.moveTo(x - 3, y - 3)
        p.lineTo(x - 3, y + h + 3)
        p.lineTo(x + w + 3, y + h + 3)

        p.lineTo(x + w + 3, y - 3)
        p.lineTo(x - 3, y - 3)
        #c.drawPath(p, fill = 0, stroke = 1)
    else:
        print("mode", mode)
    return

if sys.platform[0] == 'l':
    path = '/home/jan/git/Paintings'
if sys.platform[0] == 'w':
    path = "C:/Users/janbo/OneDrive/Documents/GitHub/Paintings"
os.chdir(path)
pdfmetrics.registerFont(TTFont('Ubuntu', 'Ubuntu-Regular.ttf'))
pdfmetrics.registerFont(TTFont('UbuntuBold', 'Ubuntu-Bold.ttf'))
pdfmetrics.registerFont(TTFont('UbuntuItalic', 'Ubuntu-Italic.ttf'))
pdfmetrics.registerFont(TTFont('UbuntuBoldItalic', 'Ubuntu-BoldItalic.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerif', 'LiberationSerif-Regular.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifBold', 'LiberationSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifItalic', 'LiberationSerif-Italic.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifBoldItalic', 'LiberationSerif-BoldItalic.ttf'))
pdfmetrics.registerFont(TTFont('DancingScript', 'DancingScript-Regular.ttf'))
pdfmetrics.registerFont(TTFont('DancingScriptBold', 'DancingScript-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DancingScriptItalic', 'DancingScript-Regular.ttf'))
pdfmetrics.registerFont(TTFont('DancingScriptBoldItalic', 'DancingScript-Bold.ttf'))
pdfmetrics.registerFont(TTFont('CormorantGaramond', 'CormorantGaramond-Regular.ttf'))
pdfmetrics.registerFont(TTFont('CormorantGaramondBold', 'CormorantGaramond-Bold.ttf'))
pdfmetrics.registerFont(TTFont('CormorantGaramondItalic', 'CormorantGaramond-Italic.ttf'))
pdfmetrics.registerFont(TTFont('CormorantGaramondBoldItalic', 'CormorantGaramond-BoldItalic.ttf'))
file_to_open = "Data/100paintings.csv"
with open(file_to_open, 'r') as file:
    csvreader = csv.reader(file, delimiter = ';')
    count = 0
    for row in csvreader:
        paintingsdata.append(row)
        print(count, paintingsdata[count][9])
        count += 1
pagewidthportrait = A4[0]
pageheightportrait = A4[1] 
pagewidthlandscape = A4[1]
pageheightlandscape = A4[0]
index = 1
strindex = "{:03d}".format(index)
painting = "Paintings/" + paintingsdata[index][0] + ".jpg"
I = Image(painting)
w = I.drawWidth / 10
h = I.drawHeight / 10
sc = float(paintingsdata[index][2])
if h >= w:
    c = canvas.Canvas("PDF/100paintings" + strindex + ".pdf", (portrait(A4)))
    c.linearGradient(0, 0, pagewidthportrait, pageheightportrait, (HexColor("#3f5d82"), HexColor("#4f73a1")))
    c.rect(0, 0, pagewidthportrait, pageheightportrait)
    x = centerportrait[0] - w * 0.5 * sc
    y = centerportrait[1] - h * 0.5 * sc
else:
    c = canvas.Canvas("PDF/100paintings" + strindex + ".pdf", (landscape(A4)))
    c.linearGradient(0, 0, pagewidthlandscape, pageheightlandscape, (HexColor("#3f5d82"), HexColor("#4f73a1")))
    c.rect(0, 0, pagewidthlandscape, pageheightlandscape)
    x = centerlandscape[0] - w * 0.5 * sc
    y = centerlandscape[1] - h * 0.5 * sc
c.setTitle(paintingsdata[index][0])
c.saveState()
c.translate(x, y)
c.scale(sc, sc)
c.drawImage(painting, 0, 0, width = w, height = h, mask='auto')
c.restoreState()
add_frame(c, paintingsdata[index][3], x, y, w * sc, h * sc, brown, gold)
c.setFillColor(HexColor('#FFFFFF'))
c.setFont(paintingfont, 25)
c.drawString(x + 50.0, y - 30.0, paintingsdata[index][0])
painter = "Painters/" + paintingsdata[index][1] + ".jpg"
infox = 100
c.drawImage(painter, infox - 20, infoyline - 110, width = 77, height = 100, mask='auto')
c.setFillColor(HexColor('#FFFFFF'))
c.setFont(paintingfont, 20)
c.drawString(infox - 50,  infoyline, paintingsdata[index][1])
c.drawString(infox + 100, infoyline - 100.0, paintingsdata[index][7])
c.drawString(infox + 100, infoyline - 70.0, paintingsdata[index][8])
c.drawString(infox + 100, infoyline - 40.0, paintingsdata[index][9])
c.save()
key = input("Wait")
