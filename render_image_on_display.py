from display_image_on_inky import display_image_from_file_on_inky
from resize_and_crop_image import resize_and_crop_image

def render_image_on_display(file_path: str):
    """Resize and display an image on the Inky Impression."""
    # Define the resized file path
    resized_path = "./images/resized_" + file_path.split("/")[-1]
    print(f"Original image path: {file_path}")
    print(f"Resized image path: {resized_path}")

    # Resize and crop the image to fit the Inky display
    resize_and_crop_image(file_path, resized_path)

    # Load the resized image and display it
    display_image_from_file_on_inky(resized_path)