import openai
import feedparser
import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()


client = OpenAI()

# Fetch the OpenAI API key from the environment
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("Please set the OPENAI_API_KEY in your .env file.")

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
        size="1024x1024",
        quality="standard"
    )

    # Get the URL of the generated image
    image_url = response.data[0].url
    return image_url

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

# Example usage:
rss_url = 'https://feeds.nos.nl/nosnieuwsalgemeen'
image_url = generate_image_from_rss_headline(rss_url)
print("Generated Image URL:", image_url)

# Download the image locally for further modification
download_image(image_url, "generated_image.png")
