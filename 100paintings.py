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
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image

paintingsdata = []
paintingfont = "LiberationSerif"

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

def add_frame(image_path, frame_width=50, frame_color=(139, 69, 19)):
    framed_img = None
    try:
        img = Image.open(image_path).convert("RGB")
        framed_img = ImageOps.expand(img, border=frame_width, fill=frame_color)
        draw = ImageDraw.Draw(framed_img)
        inner_margin = 5
        for i in range(inner_margin):
            draw.rectangle(
                [frame_width - i, frame_width - i,
                 framed_img.width - frame_width + i - 1,
                 framed_img.height - frame_width + i - 1],
                outline=(218, 165, 32)  # Golden color
            )
        return framed_img
    except FileNotFoundError:
        print("Error: The specified image file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

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
index = 2
strindex = "{:03d}".format(index)
painting = "Paintings/" + paintingsdata[index][0] + ".jpg"
I = Image(painting)
w = I.drawWidth / 10
h = I.drawHeight / 10
x = float(paintingsdata[index][2])
y = float(paintingsdata[index][3])
sc = float(paintingsdata[index][6])
if h >= w:
    c = canvas.Canvas("PDF/100paintings" + strindex + ".pdf", (portrait(A4)))
    c.linearGradient(0, 0, pagewidthportrait, pageheightportrait, (HexColor("#3f5d82"), HexColor("#4f73a1")))
    c.rect(0, 0, pagewidthportrait, pageheightportrait)
else:
    c = canvas.Canvas("PDF/100paintings" + strindex + ".pdf", (landscape(A4)))
    c.linearGradient(0, 0, pagewidthlandscape, pageheightlandscape, (HexColor("#3f5d82"), HexColor("#4f73a1")))
    c.rect(0, 0, pagewidthlandscape, pageheightlandscape)
c.setTitle(paintingsdata[index][0])
c.saveState()
c.translate(x, y)
c.scale(sc, sc)
c.drawImage(painting, 0, 0, width = w, height = h, mask='auto')
c.restoreState()
painter = "Painters/" + paintingsdata[index][1] + ".jpg"
c.drawImage(painter, x - 20, y - 150, width = 77, height = 100, mask='auto')
c.setFillColor(HexColor('#FFFFFF'))
c.setFont(paintingfont, 20)
c.drawString(x + 5.0, y - 20.0, paintingsdata[index][0])
c.drawString(x - 20, y - 170.0, paintingsdata[index][1])
c.drawString(x + 140, y - 110.0, paintingsdata[index][7])
c.drawString(x + 140, y - 140.0, paintingsdata[index][8])
c.drawString(x + 140, y - 170.0, paintingsdata[index][9])
c.save()
key = input("Wait")
