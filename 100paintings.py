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
from reportlab.pdfbase.pdfmetrics import registerFontFamily

paintingsdata = []
paintingfont = "LiberationSerif"
#pagesize=(595.27, 841.89)
centerportrait = (297.635, 495.945)
centerlandscape = (420.945, 372.638)
infoyline = 150
#centeryportait 841.89 - 150 = 691.89 / 2 = 345.945 + 150 = 495.945
#centerylandscape 595.27 - 150 = 445.27 / 2 = 222.635 + 150 = 372.638
linesmode = False

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
    
def hex_to_rgb(hex_color):
    if not isinstance(hex_color, str):
        raise ValueError("HEX color must be a string.")
    hex_color = hex_color.strip().lstrip('#')
    # Validate length (3 or 6 characters)
    if len(hex_color) not in (3, 6):
        raise ValueError("HEX color must be 3 or 6 characters long.")
    # Expand shorthand HEX (#abc → #aabbcc)
    if len(hex_color) == 3:
        hex_color = ''.join([c * 2 for c in hex_color])
    try:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
    except ValueError:
        raise ValueError("HEX color contains invalid characters.")
    return (r, g, b)
    
def darken_rgb(color, factor):
    if not (isinstance(color, tuple) and len(color) == 3):
        raise ValueError("Color must be a tuple of 3 integers (R, G, B).")
    if not all(isinstance(c, int) and 0 <= c <= 255 for c in color):
        raise ValueError("Each RGB component must be an integer between 0 and 255.")
    if not (0 < factor <= 1):
        raise ValueError("Factor must be between 0 (exclusive) and 1 (inclusive).")
    # Multiply each channel by factor and clamp to 0–255
    return tuple(max(0, min(255, int(c * factor))) for c in color)
   
def rgb_to_hex(r, g, b):
    if not all(isinstance(v, int) for v in (r, g, b)):
        raise TypeError("RGB values must be integers.")
    # Validate range
    if not all(0 <= v <= 255 for v in (r, g, b)):
        raise ValueError("RGB values must be between 0 and 255.")
    # Format as HEX string  
    return "#{:02X}{:02X}{:02X}".format(r, g, b)

def draw_frame(c, mode, x, y, w, h,  color1, color2):
    if mode == "0":
        return
    color1hex = HexColor(color1)
    color2hex = HexColor(color2)
    color2rgb = hex_to_rgb(color2)
    color2darker = darken_rgb(color2rgb, 0.8)
    color2darkerhex = rgb_to_hex(color2darker[0], color2darker[1], color2darker[2])
    if mode == "1":
        fr1w = 6
        fr1d = fr1w / 2
        c.setLineCap(2)
        c.setStrokeColor(color2hex)
        c.setLineWidth(fr1w)
        p = c.beginPath()
        p.moveTo(x - fr1d, y - fr1d)
        p.lineTo(x - fr1d, y + h + fr1d)
        p.lineTo(x + w + fr1d, y + h + fr1d)
        p.lineTo(x + w + fr1d, y - fr1d)
        p.lineTo(x - fr1d, y - fr1d)
        c.drawPath(p, fill = 0, stroke = 1)
        c.setStrokeColor(color2darkerhex)
        p = c.beginPath()
        p.moveTo(x + fr1d, y + h + fr1d)
        p.lineTo(x + w + fr1d, y + h + fr1d)
        p.lineTo(x + w + fr1d, y + fr1d)
        c.drawPath(p, fill = 0, stroke = 1)
        c.setLineWidth(1)
        c.setFillColor(color2darkerhex)
        p = c.beginPath()
        p.moveTo(x - fr1w, y + h + fr1w)
        p.lineTo(x, y + h + fr1w)
        p.lineTo(x, y + h)
        p.lineTo(x - fr1w, y + h + fr1w)
        c.drawPath(p, fill = 1, stroke = 0)
        p = c.beginPath()
        p.moveTo(x + w, y)
        p.lineTo(x + w + fr1w, y)
        p.lineTo(x + w + fr1w, y - fr1w)
        p.lineTo(x + w, y)
        c.drawPath(p, fill = 1, stroke = 0)
        fr2w = 10
        fr2d = fr2w / 2 + 6
        c.setLineCap(2)
        c.setStrokeColor(color1hex)
        c.setLineWidth(fr2w)
        p = c.beginPath()
        p.moveTo(x - fr2d, y - fr2d)
        p.lineTo(x - fr2d, y + h + fr2d)
        p.lineTo(x + w + fr2d, y + h + fr2d)
        p.lineTo(x + w + fr2d, y - fr2d)
        p.lineTo(x - fr2d, y - fr2d)
        c.drawPath(p, fill = 0, stroke = 1)
    elif mode == "2":
        c.setLineCap(2)
        c.setStrokeColor(color2hex)
        c.setLineWidth(10)
        p = c.beginPath()
        p.moveTo(x - 5, y - 5)
        p.lineTo(x - 5, y + h + 5)
        p.lineTo(x + w + 5, y + h + 5)
        p.lineTo(x + w + 5, y - 5)
        p.lineTo(x - 5, y - 5)
        c.drawPath(p, fill = 0, stroke = 1)
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
index = 35
margin = 75
strindex = "{:03d}".format(index)
painting = "Paintings/" + paintingsdata[index][0] + ".jpg"
I = Image(painting)
w = I.drawWidth / 10
h = I.drawHeight / 10
sc = float(paintingsdata[index][2])
if h >= 0.75 * w:
    c = canvas.Canvas("PDF/100paintings" + strindex + ".pdf", (portrait(A4)))
    c.linearGradient(0, 0, pagewidthportrait, pageheightportrait, (HexColor("#3f5d82"), HexColor("#4f73a1")))
    c.rect(0, 0, pagewidthportrait, pageheightportrait)
    x = centerportrait[0] - w * 0.5 * sc
    y = centerportrait[1] - h * 0.5 * sc
    if linesmode:
        c.line(margin, 0, margin, 841.89)
        c.line(0, 841.89 - margin, 595.27, 841.89 - margin)
        c.line(0, infoyline, 595.27, infoyline)
else:
    c = canvas.Canvas("PDF/100paintings" + strindex + ".pdf", (landscape(A4)))
    c.linearGradient(0, 0, pagewidthlandscape, pageheightlandscape, (HexColor("#3f5d82"), HexColor("#4f73a1")))
    c.rect(0, 0, pagewidthlandscape, pageheightlandscape)
    x = centerlandscape[0] - w * 0.5 * sc
    y = centerlandscape[1] - h * 0.5 * sc
    if linesmode:
        c.line(margin, 0, margin, 595.27)
        c.line(0, 595.27 - margin, 841.89, 595.27 - margin)
        c.line(0, infoyline, 841.89, infoyline)
c.setTitle(paintingsdata[index][0])
c.saveState()
c.translate(x, y)
c.scale(sc, sc)
c.drawImage(painting, 0, 0, width = w, height = h, mask='auto')
c.restoreState()
draw_frame(c, paintingsdata[index][3], x, y, w * sc, h * sc, paintingsdata[index][4], paintingsdata[index][5])
c.setFillColor(HexColor('#FFFFFF'))
c.setFont(paintingfont, 25)
namewidth = pdfmetrics.stringWidth(paintingsdata[index][0], paintingfont, 25)
c.drawString(x + 0.5 * (w * sc - namewidth), y - 35.0, paintingsdata[index][0])
painter = "Painters/" + paintingsdata[index][1] + ".jpg"
infox = 50
c.drawImage(painter, infox, infoyline - 140, width = 115.5, height = 150, mask='auto')
c.setFillColor(HexColor('#FFFFFF'))
c.setFont(paintingfont, 22)
c.drawString(infox + 125, infoyline - 20, paintingsdata[index][1])
c.setFont(paintingfont, 20)
c.drawString(infox + 125, infoyline - 100.0, paintingsdata[index][7])
c.drawString(infox + 125, infoyline - 75.0, paintingsdata[index][8])
c.drawString(infox + 125, infoyline - 50.0, paintingsdata[index][9])
c.save()
key = input("Wait")
