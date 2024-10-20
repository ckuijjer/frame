from rss_feed import fetch_rss_feed
from image_generation import generate_image_from_summary
from image_io import download_image
from image_processing import resize_and_crop_image
from text_processing import add_title_to_image
from utils import get_filename
from config import DEFAULT_IMAGE_SIZE, PADDING

def main():
    rss_url = 'https://feeds.nos.nl/nosnieuwsalgemeen'
    title, summary = fetch_rss_feed(rss_url)
    print(f"Fetched article: {title}")

    image_url = generate_image_from_summary(title, summary)
    print(f"Generated Image URL: {image_url}")

    # Save images in the images/ subdirectory
    filename = get_filename(title)  # Uses the images/ directory by default
    download_image(image_url, filename)

    resized_filename = f"resized_{filename}"
    resize_and_crop_image(filename, resized_filename, DEFAULT_IMAGE_SIZE)

    output_filename_with_text = f"with_text_{resized_filename}"
    add_title_to_image(resized_filename, output_filename_with_text, title, DEFAULT_IMAGE_SIZE, PADDING)

if __name__ == '__main__':
    main()
