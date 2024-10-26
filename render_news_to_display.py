import os
from fetch_rss_feed import fetch_rss_feed
from generate_image import generate_image
from download_image import download_image
from resize_and_crop_image import resize_and_crop_image
from text_processing import add_title_to_image
from display_image_on_inky import display_image_on_inky
from utils import get_filename
from config import DEFAULT_IMAGE_SIZE, PADDING

def render_news_to_display(provider="getimg"):
    rss_url = 'https://feeds.nos.nl/nosnieuwsalgemeen'
    title, summary = fetch_rss_feed(rss_url)
    print(f"Fetched article: {title}")

    # Generate the original filename
    filename = get_filename(title)
    
    # Check if the image already exists in the images/ directory
    if os.path.exists(filename):
        print(f"Image already exists: {filename}")
    else:
        # Generate the image if it doesn't already exist
        image_url = generate_image(title, summary, provider=provider)
        print(f"Generated Image URL: {image_url}")
        download_image(image_url, filename)

    # Generate the resized and text-enhanced filenames with suffixes
    resized_filename = get_filename(title, suffix="_resized")
    output_filename_with_text = get_filename(title, suffix="_with_text_resized")

    # Resize the image
    resize_and_crop_image(filename, resized_filename, DEFAULT_IMAGE_SIZE)

    # Add title to the resized image
    add_title_to_image(resized_filename, output_filename_with_text, title, DEFAULT_IMAGE_SIZE, PADDING)

    # Display the image on the Inky Impression (or print a message if not on Linux)
    display_image_on_inky(output_filename_with_text)

if __name__ == "__main__":
    render_news_to_display()