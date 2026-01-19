from PIL import Image, ImageOps, ImageDraw
import sys
import os

def add_frame(image_path, output_path, frame_width=50, frame_color=(139, 69, 19)):
    """
    Adds a decorative frame around an image.
    
    :param image_path: Path to the input image
    :param output_path: Path to save the framed image
    :param frame_width: Width of the frame in pixels
    :param frame_color: RGB tuple for frame color
    """
    try:
        # Open the image
        img = Image.open(image_path).convert("RGB")

        # Add a solid color border (frame)
        framed_img = ImageOps.expand(img, border=frame_width, fill=frame_color)

        # Optional: Add an inner golden border for elegance
        draw = ImageDraw.Draw(framed_img)
        inner_margin = 5
        for i in range(inner_margin):
            draw.rectangle(
                [frame_width - i, frame_width - i,
                 framed_img.width - frame_width + i - 1,
                 framed_img.height - frame_width + i - 1],
                outline=(218, 165, 32)  # Golden color
            )

        # Save the result
        framed_img.save(output_path)
        print(f"Framed image saved to: {output_path}")

    except FileNotFoundError:
        print("Error: The specified image file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    if sys.platform[0] == 'l':
        path = '/home/jan/git/Paintings'
    if sys.platform[0] == 'w':
        path = "C:/Users/janbo/OneDrive/Documents/GitHub/Paintings"
    os.chdir(path)
    # Change these paths to your own image and output location
    input_image = "Paintings/painting.jpg"  # Replace with your image file
    output_image = "PDF/framed_painting.jpg"

    if not os.path.exists(input_image):
        print(f"Input image '{input_image}' not found. Please place it in the script folder.")
        sys.exit(1)

    add_frame(input_image, output_image, frame_width=60, frame_color=(101, 67, 33))
    key = input("Wait")
