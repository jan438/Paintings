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
    
 
colhex = "#a1d3f1"
colrgb = hex_to_rgb(colhex)
coldarker = darken_rgb(colrgb, 0.6)
coldarkerhex = rgb_to_hex(coldarker[0], coldarker[1], coldarker[2])
print(coldarkerhex)
key = input("Wait")
