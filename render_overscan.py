from PIL import Image, ImageDraw, ImageFont
from config import DEFAULT_IMAGE_SIZE
from display_image_on_inky import display_image_on_inky

def render_overscan(top: int, right: int, bottom: int, left: int):
    # Define image parameters and grid settings with vertical display for x and y coordinates
    width, height = DEFAULT_IMAGE_SIZE
    grid_spacing = 50

    # Create a white background image
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # Load a smaller font size
    font = ImageFont.load_default()

    # Draw the grid and add coordinates with vertical alignment for x and y separately
    for x in range(0, width + 1, grid_spacing):
        for y in range(0, height + 1, grid_spacing):
            # Draw horizontal and vertical lines
            draw.line((x, 0, x, height), fill="gray", width=1)
            draw.line((0, y, width, y), fill="gray", width=1)
            
            # Draw the x and y coordinates separately, aligned vertically
            draw.text((x + 5, y + 5), str(x), fill="black", font=font)   # X coordinate
            draw.text((x + 5, y + 20), str(y), fill="black", font=font)  # Y coordinate, below X

    # Draw a red rectangle with a 4px border width
    border_width = 4
    draw.rectangle([(left, top), (right, bottom)], outline="red", width=border_width)

    # Display the image
    display_image_on_inky(image)