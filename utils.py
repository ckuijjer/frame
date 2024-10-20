import re
from datetime import datetime
import os

def snake_case(text: str) -> str:
    """Converts a given string to snake_case."""
    return re.sub(r'[\W_]+', '_', text).strip().lower()

def get_filename(title: str, directory: str = "images", prefix: str = "") -> str:
    """
    Generate a filename based on the current date and the article title, with an optional prefix, and store it in the images directory.
    
    Args:
        title (str): The article title.
        directory (str): The directory where the images will be stored. Defaults to 'images'.
        prefix (str): Optional prefix to add to the filename (e.g., "resized_", "with_text_").
    
    Returns:
        str: The full path of the generated filename.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

    current_date = datetime.now().strftime("%Y-%m-%d")
    snake_case_title = snake_case(title)
    filename = f"{prefix}{current_date}_{snake_case_title}.png"
    return os.path.join(directory, filename)
