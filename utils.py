import re
from datetime import datetime

def snake_case(text: str) -> str:
    """
    Converts a given string to snake_case.
    
    Args:
        text (str): Input string to be converted.
    
    Returns:
        str: Snake_case formatted string.
    """
    return re.sub(r'[\W_]+', '_', text).strip().lower()

def get_filename(title: str) -> str:
    """
    Generate a filename based on the current date and the article title.
    
    Args:
        title (str): The article title.
    
    Returns:
        str: A snake_case filename with the current date.
    """
    current_date = datetime.now().strftime("%Y-%m-%d")
    snake_case_title = snake_case(title)
    return f"{current_date}_{snake_case_title}.png"
