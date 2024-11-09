from PIL import Image, ImageOps
from typing import Tuple
from config import DEFAULT_IMAGE_SIZE, OVERSCAN_TOP, OVERSCAN_RIGHT, OVERSCAN_BOTTOM, OVERSCAN_LEFT

def resize_and_crop_image(input_path: str, output_path: str, target_size: Tuple[int, int]):
    """
    Resize and crop an image to fit the target size while maintaining aspect ratio.
    
    Args:
        input_path (str): Path to the input image.
        output_path (str): Path to save the resized image.
    """
    try:
        # Calculate the dimensions of the visible area based on absolute coordinates
        visible_width = OVERSCAN_RIGHT - OVERSCAN_LEFT
        visible_height = OVERSCAN_BOTTOM - OVERSCAN_TOP

        with Image.open(input_path) as img:
            img = ImageOps.fit(img, (visible_width, visible_height), Image.LANCZOS, centering=(0.5, 0.5))

            # Create a blank (white) 800x480 background
            background = Image.new("RGB", target_size, "white")

            # Paste the resized image within the defined visible area
            paste_position = (OVERSCAN_LEFT, OVERSCAN_TOP)
            # background.paste(img, paste_position)

            background.save(output_path, overwrite=True)
            print(f"Image successfully resized and cropped to: {output_path}")
    except Exception as e:
        print(f"Error resizing and cropping image: {e}")
