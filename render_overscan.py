from PIL import Image, ImageDraw, ImageFont
from config import DEFAULT_IMAGE_SIZE
from display_image_on_inky import display_image_on_inky

def render_overscan_grid():
    width, height = DEFAULT_IMAGE_SIZE
    image = Image.new("RGB", DEFAULT_IMAGE_SIZE, "white")
    draw = ImageDraw.Draw(image)

    # Draw the grid
    grid_spacing = 100
    for x in range(0, width, grid_spacing):
        draw.line((x, 0, x, height), fill="gray", width=1)
    for y in range(0, height, grid_spacing):
        draw.line((0, y, width, y), fill="gray", width=1)

    # Centered axis in the middle of the image
    center_x, center_y = width // 2, height // 2
    draw.line((center_x, 0, center_x, height), fill="black", width=2)
    draw.line((0, center_y, width, center_y), fill="black", width=2)

    # Add numbers to the axes every 100 pixels
    font = ImageFont.load_default()  # Use a default font for simplicity
    for x in range(0, width, grid_spacing):
        draw.text((x, center_y + 5), str(x - center_x), fill="black", font=font)
    for y in range(0, height, grid_spacing):
        draw.text((center_x + 5, y), str(y - center_y), fill="black", font=font)

    # Display the image
    display_image_on_inky(image)

# def resize_and_crop_image(input_path: str, output_path: str, target_size: Tuple[int, int]):
def render_overscan_frame(top: int, left: int, bottom: int, right: int):
    image = Image.new("RGB", DEFAULT_IMAGE_SIZE, "white")
    draw = ImageDraw.Draw(image)

    # Draw a red rectangle with a 4px border width
    border_width = 4
    draw.rectangle([(top, left), (bottom, right)], outline="red", width=border_width)

    display_image_on_inky(image)
