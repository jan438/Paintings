import drawsvg as draw
import math

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

# Decorative pattern: animated circles along the frame
num_circles = 40
radius = 8
for i in range(num_circles):
    angle = (2 * math.pi / num_circles) * i
    # Position circles along a square path
    if i < num_circles // 4:
        x = -width/2 + frame_thickness/2
        y = -height/2 + (i / (num_circles/4)) * (height - frame_thickness)
    elif i < num_circles // 2:
        x = -width/2 + frame_thickness/2 + ((i - num_circles/4) / (num_circles/4)) * (width - frame_thickness)
        y = height/2 - frame_thickness/2
    elif i < 3*num_circles // 4:
        x = width/2 - frame_thickness/2
        y = height/2 - frame_thickness/2 - ((i - num_circles/2) / (num_circles/4)) * (height - frame_thickness)
    else:
        x = width/2 - frame_thickness/2 - ((i - 3*num_circles/4) / (num_circles/4)) * (width - frame_thickness)
        y = -height/2 + frame_thickness/2

    circle = draw.Circle(x, y, radius, fill='gold', stroke='black', stroke_width=1)
    # Animate color
    circle.append_anim(draw.Animate('fill', '2s', values='gold;orange;gold', repeatCount='indefinite'))
    d.append(circle)

# Save SVG
d.save_svg('PDF/dynamic_frame.svg')

# Optional: Save as PNG (requires CairoSVG installed)
try:
    d.save_png('dynamic_frame.png')
except Exception as e:
    print("PNG export skipped (CairoSVG not installed):", e)

print("SVG frame created: dynamic_frame.svg")
key = input("Wait")
