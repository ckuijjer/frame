import openai
import requests
from config import OPENAI_API_KEY, GETIMG_API_KEY, DEFAULT_IMAGE_SIZE

# Set the OpenAI API key
openai.api_key = OPENAI_API_KEY

client = openai.OpenAI()

def generate_image(title: str, summary: str, provider="openai") -> str:
    """
    Generate an image using based title and summary.
    
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

    print(f"Generating image with prompt: |{prompt}|")
    if provider == "openai":
        return generate_image_from_openai(prompt)
    elif provider == "getimg":
        return generate_image_from_getimg(prompt)
    else:
        raise ValueError("Invalid provider. Choose 'openai' or 'getimg'.")

def generate_image_from_openai(prompt: str) -> str:
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1792x1024",
        quality="standard"
    )

    image_url = response.data[0].url
    return image_url

def generate_image_from_getimg(prompt: str) -> str:
    url = "https://api.getimg.ai/v1/stable-diffusion-xl/text-to-image"
    payload = {
        "model": "stable-diffusion-xl-v1-0",
        "prompt": prompt,
        "width": DEFAULT_IMAGE_SIZE[0],
        "height": DEFAULT_IMAGE_SIZE[1],
        "steps": 30,
        "response_format": "url"
    }
    headers = {
        "Authorization": f"Bearer {GETIMG_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()["url"]
    else:
        raise Exception(f"Failed to generate image with getimg.ai: {response.status_code}, {response.text}")
