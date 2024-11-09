import platform
import os
from PIL import Image, ImageOps, ImageFile

def display_image_from_file_on_inky(image_path: str):
    """
    Display an image on the Inky Impression if the OS is Linux.
    If the OS is not Linux, print a message that the image will not be displayed.
    
    Args:
        image_path (str): The path to the image file to display.
    """
    if platform.system() != 'Linux':
        print(f"Cannot display image on Inky Impression: Not running on Linux. Image path: {image_path}")
        return
    
    # Check if the image file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file {image_path} not found")

    print(f'Displaying {image_path}')
    image = Image.open(image_path)

    display_image_on_inky(image)

def display_image_on_inky(image: Image):
    if platform.system() != 'Linux':
        print(f"Cannot display image on Inky Impression: Not running on Linux.")
        return

    from inky.auto import auto  # Only import inky if running on Linux
    inky = auto()

    SATURATION = 0.5
    BORDER_COLOR = inky.WHITE
    RESAMPLING = Image.BICUBIC

    # Resize the image to fit the Inky display's resolution
    resized_image = ImageOps.pad(image, inky.resolution, method=RESAMPLING, color=BORDER_COLOR)
    
    # Set image on the Inky display
    inky.set_image(resized_image, saturation=SATURATION)
    inky.set_border(BORDER_COLOR)
    inky.show()

