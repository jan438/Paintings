import drawsvg as draw
import math
import sys
import os
import csv
from PIL import Image, ImageOps, ImageDraw
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch, mm
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.utils import ImageReader

paintingsdata = []

def add_frame(image_path, output_path, frame_width=50, frame_color=(139, 69, 19)):
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
        framed_img.save(output_path)
        print(f"Framed image saved to: {output_path}")
    except FileNotFoundError:
        print("Error: The specified image file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

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
    if i == 1:
        break
    input_image = "Paintings/" + paintingsdata[i][0] + ".jpg"
    output_image = "PDF/" + paintingsdata[i][0] + ".jpg"
    if not os.path.exists(input_image):
        print(f"Input image '{input_image}' not found. Please place it in the script folder.")
    else:
        add_frame(input_image, output_image, frame_width=60, frame_color=(101, 67, 33))
        logo = ImageReader(output_image)
        c.drawImage(logo, 10, 10, mask='auto')
        c.drawString(10, 200 - i * 30, paintingsdata[i][0])
    c.save()
key = input("Wait")
