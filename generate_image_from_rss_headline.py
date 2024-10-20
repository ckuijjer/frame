import openai
import feedparser
import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
import re
from datetime import datetime
from PIL import ImageFont, ImageDraw, Image, ImageOps
import platform

# Load environment variables from .env file
load_dotenv()

client = OpenAI()

# Fetch the OpenAI API key from the environment
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("Please set the OPENAI_API_KEY in your .env file.")

def snake_case(text):
    """Converts a given string to snake_case."""
    return re.sub(r'[\W_]+', '_', text).strip().lower()

def fetch_rss_feed(rss_url):
    """Retrieve the RSS feed and return the title and summary of the first article."""
    feed = feedparser.parse(rss_url)
    first_article = feed.entries[0]
    title = first_article.title
    summary = first_article.summary
    return title, summary

def generate_image_from_summary(title, summary):
    """Generate an image using OpenAI's DALL·E API based on the title and summary."""
    # Get the first two paragraphs from the summary
    paragraphs = summary.split('</p>')
    first_paragraph = paragraphs[0] if len(paragraphs) > 0 else ''
    second_paragraph = paragraphs[1] if len(paragraphs) > 1 else ''
    
    # Combine title and paragraphs to create a prompt
    prompt = f"Generate an image based on the news article titled: '{title}'. The content begins with: '{first_paragraph} {second_paragraph}'."

    # Call the OpenAI DALL·E API to generate an image
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1792x1024",
        quality="standard"
    )

    # Get the URL of the generated image
    image_url = response.data[0].url
    return image_url

def download_image(image_url, filename):
    """Download the generated image from the URL."""
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Image successfully downloaded: {filename}")
    else:
        print("Failed to download image.")

def resize_and_crop_image(input_path, output_path, target_size):
    """Resize and crop an image to fit the target size while maintaining aspect ratio."""
    try:
        with Image.open(input_path) as img:
            img = ImageOps.fit(img, target_size, Image.LANCZOS, centering=(0.5, 0.5))
            img.save(output_path)
            print(f"Image successfully resized and cropped to: {output_path}")
    except Exception as e:
        print(f"Error resizing and cropping image: {e}")

def wrap_text(draw, text, font, max_width):
    """Wrap text to fit within the specified width, considering font size."""
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

def add_title_to_image(input_path, output_path, text, max_width, max_height, padding, font_path=None):
    """Superimpose left-aligned text with black outline on the image."""
    try:
        with Image.open(input_path) as img:
            draw = ImageDraw.Draw(img)

            padded_max_width = max_width - 2 * padding
            padded_max_height = max_height - 2 * padding

            if font_path:
                font = ImageFont.truetype(font_path, 50)
            else:
                font = ImageFont.load_default()

            font_size = 50
            preferred_lines = 3
            while True:
                font = ImageFont.truetype(font_path or "arial.ttf", font_size)
                lines = wrap_text(draw, text, font, padded_max_width)

                if len(lines) > preferred_lines:
                    font_size -= 2
                else:
                    line_height = font.getbbox("hg")[3]
                    total_text_height = line_height * len(lines)

                    if total_text_height <= padded_max_height:
                        break
                    else:
                        font_size -= 2

                if font_size < 30:
                    if preferred_lines > 1:
                        preferred_lines -= 1
                        font_size = 50
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

def get_font_path():
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

# # Example usage:
rss_url = 'https://feeds.nos.nl/nosnieuwsalgemeen'
title, summary = fetch_rss_feed(rss_url)
image_url = generate_image_from_summary(title, summary)
print("Generated Image URL:", image_url)

current_date = datetime.now().strftime("%Y-%m-%d")
snake_case_title = snake_case(title)
filename = f"{current_date}_{snake_case_title}.png"

# Download the image locally
download_image(image_url, filename)

# Resize the image
target_size = (800, 480)
resized_filename = f"resized_{filename}"
resize_and_crop_image(filename, resized_filename, target_size)

# Superimpose the title on the resized image
output_filename_with_text = f"with_text_{resized_filename}"
font_path = get_font_path()
add_title_to_image(resized_filename, output_filename_with_text, title, max_width=800, max_height=120, padding=20, font_path=font_path)
