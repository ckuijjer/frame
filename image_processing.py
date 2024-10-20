import openai
import requests
from PIL import Image, ImageFont, ImageDraw, ImageOps
from typing import Tuple
import platform
from config import PREFERRED_LINES, DEFAULT_FONT_SIZE, MIN_FONT_SIZE

client = openai.OpenAI()

def generate_image_from_summary(title: str, summary: str) -> str:
    """
    Generate an image using OpenAI's DALL·E API based on the title and summary.
    
    Args:
        title (str): The title of the article.
        summary (str): The summary of the article.
    
    Returns:
        str: URL of the generated image.
    """
    paragraphs = summary.split('</p>')
    first_paragraph = paragraphs[0] if len(paragraphs) > 0 else ''
    second_paragraph = paragraphs[1] if len(paragraphs) > 1 else ''
    
    prompt = f"Generate an image based on the news article titled: '{title}'. The content begins with: '{first_paragraph} {second_paragraph}'."

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1792x1024",
        quality="standard"
    )

    image_url = response.data[0].url
    return image_url

def download_image(image_url: str, filename: str):
    """Download the generated image from the URL."""
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Image successfully downloaded: {filename}")
    else:
        print("Failed to download image.")

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

def wrap_text(draw: ImageDraw.Draw, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    """
    Wrap text to fit within the specified width, considering font size.
    
    Args:
        draw (ImageDraw.Draw): The ImageDraw object used for text rendering.
        text (str): The text to wrap.
        font (ImageFont.FreeTypeFont): The font to be used.
        max_width (int): The maximum allowed width for the text.
    
    Returns:
        list: A list of wrapped text lines.
    """
    lines = []
    words = text.split(' ')
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        left, top, right, bottom = draw.textbbox((0, 0), test_line, font=font)
        text_width = right - left

        if text_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "

    lines.append(current_line)
    return lines

def add_title_to_image(input_path: str, output_path: str, text: str, target_size: Tuple[int, int], padding: int):
    """
    Superimpose left-aligned text with a black outline on the image.
    
    Args:
        input_path (str): Path to the input image.
        output_path (str): Path to save the image with the title.
        text (str): The title text to add to the image.
        target_size (tuple): The target size (width, height) of the image.
        padding (int): The padding around the text.
    """
    try:
        with Image.open(input_path) as img:
            draw = ImageDraw.Draw(img)

            max_width = target_size[0] - 2 * padding
            max_height = target_size[1] // 4 - 2 * padding

            # Get the font path based on the operating system
            font_path = get_font_path()

            if font_path:
                font = ImageFont.truetype(font_path, DEFAULT_FONT_SIZE)
            else:
                font = ImageFont.load_default()

            font_size = DEFAULT_FONT_SIZE
            preferred_lines = PREFERRED_LINES
            while True:
                font = ImageFont.truetype(font_path or "arial.ttf", font_size)
                lines = wrap_text(draw, text, font, max_width)

                if len(lines) > preferred_lines:
                    font_size -= 2
                else:
                    line_height = font.getbbox("hg")[3]
                    total_text_height = line_height * len(lines)

                    if total_text_height <= max_height:
                        break
                    else:
                        font_size -= 2

                if font_size < MIN_FONT_SIZE:
                    if preferred_lines > 1:
                        preferred_lines -= 1
                        font_size = DEFAULT_FONT_SIZE
                    else:
                        break

            y_position = img.height - total_text_height - padding
            outline_width = 2

            for line in lines:
                for x in range(-outline_width, outline_width + 1):
                    for y in range(-outline_width, outline_width + 1):
                        if x != 0 or y != 0:
                            draw.text((padding + x, y_position + y), line, font=font, fill="black")

                draw.text((padding, y_position), line, font=font, fill="white")
                y_position += line_height

            img.save(output_path)
            print(f"Text with outline successfully added to: {output_path}")
    except Exception as e:
        print(f"Error adding text to image: {e}")

def get_font_path() -> str:
    """Get the path to the Roboto font based on the operating system."""
    system = platform.system()
    if system == "Darwin":
        return "~/Library/Fonts/Roboto-Regular.ttf"
    elif system == "Linux":
        return "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-Regular.ttf"
    elif system == "Windows":
        return "C:/Windows/Fonts/Roboto-Regular.ttf"
    else:
        return None
