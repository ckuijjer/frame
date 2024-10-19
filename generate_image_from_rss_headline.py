import openai
import feedparser
import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
import re
from datetime import datetime
from PIL import ImageFont, ImageDraw, Image, ImageOps

# Load environment variables from .env file
load_dotenv()


client = OpenAI()

# Fetch the OpenAI API key from the environment
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("Please set the OPENAI_API_KEY in your .env file.")

def snake_case(text):
    """Converts a given string to snake_case."""
    # Replace non-alphanumeric characters with spaces, then replace spaces with underscores and lower the case
    return re.sub(r'[\W_]+', '_', text).strip().lower()

def generate_image_from_rss_headline(rss_url):
    # Parse the RSS feed
    feed = feedparser.parse(rss_url)

    # Get the first article
    first_article = feed.entries[0]

    # Extract the title and the first two paragraphs
    title = first_article.title
    summary = first_article.summary

    # Get the first two paragraphs
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
    return image_url, title

def download_image(image_url, filename):
    # Send a GET request to fetch the image
    response = requests.get(image_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the image to the specified file
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Image successfully downloaded: {filename}")
    else:
        print("Failed to download image.")

def resize_and_crop_image(input_path, output_path, target_size):
    """Resize and crop an image to fit the target size while maintaining aspect ratio."""
    try:
        with Image.open(input_path) as img:
            # Resize while maintaining aspect ratio
            img = ImageOps.fit(img, target_size, Image.LANCZOS, centering=(0.5, 0.5))

            # Save the resized and cropped image
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
        # Check the width of the current line with the new word added
        test_line = current_line + word + " "
        left, top, right, bottom = draw.textbbox((0, 0), test_line, font=font)
        text_width = right - left

        if text_width <= max_width:
            current_line = test_line  # If it fits, add the word
        else:
            lines.append(current_line)  # If it doesn't fit, store the line and start a new one
            current_line = word + " "

    lines.append(current_line)  # Add the last line
    return lines

def add_dynamic_text_with_padding_left_aligned(input_path, output_path, text, max_width, max_height, padding, font_path=None):
    """Superimpose left-aligned text with black outline on the image, preferring 3 lines, then 2, and 1 as a last resort."""
    try:
        with Image.open(input_path) as img:
            draw = ImageDraw.Draw(img)

            # Adjust max width and height by the padding
            padded_max_width = max_width - 2 * padding
            padded_max_height = max_height - 2 * padding

            # Load a font (use a built-in font or specify your own)
            if font_path:
                font = ImageFont.truetype(font_path, 50)  # Initial font size, we will adjust it
            else:
                font = ImageFont.load_default()

            # Try to fit the text into 3 lines first, then 2 lines, and 1 as a last resort
            font_size = 50
            preferred_lines = 3  # Start by aiming for 3 lines
            while True:
                font = ImageFont.truetype(font_path or "arial.ttf", font_size)

                # Wrap text into multiple lines considering the font size
                lines = wrap_text(draw, text, font, padded_max_width)

                # If there are more than 3 lines, reduce the font size
                if len(lines) > preferred_lines:
                    font_size -= 2
                else:
                    # Calculate total height of the text using textbbox()
                    line_height = font.getbbox("hg")[3]  # Get text height
                    total_text_height = line_height * len(lines)

                    # Ensure the total height fits within the padded max height
                    if total_text_height <= padded_max_height:
                        break
                    else:
                        font_size -= 2

                # If font size becomes too small, try reducing the preferred lines (from 3 to 2, then 1)
                if font_size < 10:  # Arbitrary lower limit on font size
                    if preferred_lines > 1:
                        preferred_lines -= 1
                        font_size = 50  # Reset font size and try again
                    else:
                        break

            # Position the text
            y_position = img.height - total_text_height - padding

            # Add a black outline to the text
            outline_width = 2  # Adjust outline thickness
            for line in lines:
                for x in range(-outline_width, outline_width + 1):
                    for y in range(-outline_width, outline_width + 1):
                        if x != 0 or y != 0:  # Avoid drawing the white text yet
                            draw.text((padding + x, y_position + y), line, font=font, fill="black")

                # Draw the white text on top
                draw.text((padding, y_position), line, font=font, fill="white")
                y_position += line_height

            # Save the final image with the superimposed text
            img.save(output_path)
            print(f"Text with outline successfully added to: {output_path}")
    except Exception as e:
        print(f"Error adding text to image: {e}")



# # Example usage:
rss_url = 'https://feeds.nos.nl/nosnieuwsalgemeen'
image_url, title = generate_image_from_rss_headline(rss_url)
print("Generated Image URL:", image_url)

# Get the current date
current_date = datetime.now().strftime("%Y-%m-%d")

# Convert the title to SnakeCase
snake_case_title = snake_case(title)

filename = f"{current_date}_{snake_case_title}.png"

# Download the image locally for further modification
download_image(image_url, filename)

# Example usage:
# Define the target size (800x480 pixels)
target_size = (800, 480)

resized_filename = f"resized_{filename}"
resize_and_crop_image(filename, resized_filename, target_size)

# Superimpose the title on the resized image
output_filename_with_text = f"with_text_{resized_filename}"
article_title = title  # You already fetched the title in the previous step

# resized_filename=f"resized_2024-10-19_bewoner_van_ontploft_huis_meppel_opgepakt.png"
# output_filename_with_text = f"with_text_resized_2024-10-19_bewoner_van_ontploft_huis_meppel_opgepakt.png"
# article_title = f"Bewoner van ontploft huis Meppel opgepakt"  # You already fetched the title in the previous step

# Ensure the text takes up the full width (800px) and max height (120px)
padding = 20

# sudo apt-get install fonts-roboto
# font_path=/usr/share/fonts/truetype/roboto/Roboto-Regular.ttf

font_path="~/Library/Fonts/Roboto-Regular.ttf"
add_dynamic_text_with_padding_left_aligned(resized_filename, output_filename_with_text, article_title, max_width=800, max_height=120, padding=padding,font_path=font_path)
