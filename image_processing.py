from PIL import Image, ImageOps
from typing import Tuple

def resize_and_crop_image(input_path: str, output_path: str, target_size: Tuple[int, int]):
    """
    Resize and crop an image to fit the target size while maintaining aspect ratio.
    
    Args:
        input_path (str): Path to the input image.
        output_path (str): Path to save the resized image.
        target_size (tuple): Target size as (width, height).
    """
    try:
        with Image.open(input_path) as img:
            img = ImageOps.fit(img, target_size, Image.LANCZOS, centering=(0.5, 0.5))
            img.save(output_path)
            print(f"Image successfully resized and cropped to: {output_path}")
    except Exception as e:
        print(f"Error resizing and cropping image: {e}")
