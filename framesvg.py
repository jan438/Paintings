import drawsvg as draw
import math
import sys
import os

if sys.platform[0] == 'l':
    path = '/home/jan/git/Paintings'
if sys.platform[0] == 'w':
    path = "C:/Users/janbo/OneDrive/Documents/GitHub/Paintings"
os.chdir(path)

# Canvas size
width, height = 500, 500

# Create a drawing
d = draw.Drawing(width, height, origin='center')

# Background
d.append(draw.Rectangle(-width/2, -height/2, width, height, fill='#f8f4e3'))

# Frame border parameters
frame_thickness = 30
frame_color = '#8b5e3c'

# Outer frame
d.append(draw.Rectangle(
    -width/2, -height/2, width, height,
    fill=frame_color, stroke='black', stroke_width=2
))

# Inner cutout (to simulate the painting area)
d.append(draw.Rectangle(
    -width/2 + frame_thickness, -height/2 + frame_thickness,
    width - 2*frame_thickness, height - 2*frame_thickness,
    fill='white'
))

# Save SVG
d.save_svg('SVG/dynamic_frame.svg')

# Optional: Save as PNG (requires CairoSVG installed)
try:
    d.save_png('dynamic_frame.png')
except Exception as e:
    print("PNG export skipped (CairoSVG not installed):", e)

print("SVG frame created: dynamic_frame.svg")
key = input("Wait")
