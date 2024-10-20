import os
import time
from inky.auto import auto
from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw
from rss_feed import fetch_rss_feed
from image_generation import generate_image_from_summary
from image_io import download_image
from image_processing import resize_and_crop_image
from text_processing import add_title_to_image
from display_on_inky import display_image_on_inky
from utils import get_filename
from config import DEFAULT_IMAGE_SIZE, PADDING

# Set up the Inky Impression (assuming PHAT variant)
inky = auto()

# Get buttons from the Inky Impression
BUTTON_A = inky.buttons.A
BUTTON_B = inky.buttons.B
BUTTON_C = inky.buttons.C
BUTTON_D = inky.buttons.D

# Function to fetch and process the selected article
def process_article(article_index):
    # Fetch the RSS feed
    rss_url = 'https://feeds.nos.nl/nosnieuwsalgemeen'
    articles = fetch_rss_feed(rss_url)
    
    if article_index >= len(articles):
        print(f"No article available for index {article_index}")
        return

    title, summary = articles[article_index]
    print(f"Selected article: {title}")

    # Generate the original filename
    filename = get_filename(title)

    # Check if the image already exists
    if not os.path.exists(filename):
        # Generate the image if it doesn't exist
        image_url = generate_image_from_summary(title, summary)
        print(f"Generated Image URL: {image_url}")
        download_image(image_url, filename)

    # Generate the resized and text-enhanced filenames
    resized_filename = get_filename(title, prefix="resized_")
    output_filename_with_text = get_filename(title, prefix="with_text_resized_")

    # Resize the image
    resize_and_crop_image(filename, resized_filename, DEFAULT_IMAGE_SIZE)

    # Add title to the resized image
    add_title_to_image(resized_filename, output_filename_with_text, title, DEFAULT_IMAGE_SIZE, PADDING)

    # Display the image on the Inky Impression
    display_image_on_inky(output_filename_with_text)

# Main loop to wait for button presses
def main():
    print("Waiting for button presses...")

    while True:
        if BUTTON_A.read():
            print("Button A pressed")
            process_article(0)  # First article
        elif BUTTON_B.read():
            print("Button B pressed")
            process_article(1)  # Second article
        elif BUTTON_C.read():
            print("Button C pressed")
            process_article(2)  # Third article
        elif BUTTON_D.read():
            print("Button D pressed")
            process_article(3)  # Fourth article

        # Wait for a short time before checking the buttons again
        time.sleep(0.1)

if __name__ == "__main__":
    main()
