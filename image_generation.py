import openai
from config import OPENAI_API_KEY

# Set the OpenAI API key
openai.api_key = OPENAI_API_KEY

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
