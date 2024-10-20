import requests

def download_image(image_url: str, filename: str):
    """Download the generated image from the URL."""
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Image successfully downloaded: {filename}")
    else:
        print("Failed to download image.")
