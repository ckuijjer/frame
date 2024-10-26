from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GETIMG_API_KEY = os.getenv("GETIMG_API_KEY")

# Default Image Size
DEFAULT_IMAGE_SIZE = (800, 480)

# Padding and Text Settings
PADDING = 20
DEFAULT_FONT_SIZE = 50
MIN_FONT_SIZE = 30
PREFERRED_LINES = 3
