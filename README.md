# **Frame**

Frame is a Python project that fetches the latest headlines from an RSS feed, generates images using OpenAI's DALL·E API, processes the images by adding article titles, and displays them on an Inky Impression e-ink display.

## **Table of Contents**

- [Pre-requisites](#pre-requisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [License](#license)

## **Pre-requisites**

Make sure your system meets the following requirements:

### **Hardware**

- Raspberry Pi with an Inky Impression e-ink display.

### **Software**

On your Raspberry Pi (or Linux machine), install the required system packages:

```bash
sudo apt install libopenblas-dev fonts-roboto
```

- **libopenblas-dev**: Required for numerical computations by libraries like NumPy.
- **fonts-roboto**: Required for adding text in the Roboto font to images.

## **Installation**

1. Clone this repository:

   ```bash
   git clone https://github.com/ckuijjer/frame.git
   cd frame
   ```

2. Set up a virtual environment for the project:

   ```bash
   python -m venv env
   source env/bin/activate
   ```

3. Install the required Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your OpenAI API key by creating a `.env` file in the root of the project:

   ```bash
   touch .env
   ```

   Add the following line to the `.env` file, replacing `your_openai_api_key_here` with your actual OpenAI API key:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## **Configuration**

### **Environment Variables**

Ensure you have the following environment variables set in your `.env` file:

- **`OPENAI_API_KEY`**: Your OpenAI API key to generate images using DALL·E.

### **Default Settings**

- The generated images will be saved in the `images/` directory.
- The RSS feed URL, image sizes, and padding can be configured directly in the code (see `config.py` for image and text settings).

## **Usage**

After installing the dependencies and setting up your environment, you can run the main script to fetch the latest headlines, generate images, and display them on your Inky Impression display:

```bash
python main.py
```

### **How It Works**

1. **Fetch RSS Feed**: The script fetches the latest headlines from the configured RSS feed (currently configured for NOS news).
2. **Generate Image**: If an image doesn't already exist for the headline, it uses OpenAI's DALL·E to generate an image based on the headline and summary.
3. **Image Processing**: The image is resized, cropped, and the title is superimposed on the image.
4. **Display on Inky Impression**: If you're running the script on a Raspberry Pi, it will display the final image on the Inky Impression e-ink display.

### **Files and Directories**

- **`images/`**: Contains all the generated images. Original, resized, and text-enhanced versions are saved in this folder.
- **`main.py`**: The main script that coordinates the entire workflow from fetching RSS feeds to displaying the images.
- **`config.py`**: Configuration settings such as image sizes, padding, and environment variables.

### **Example Workflow**

1. Run `python main.py`.
2. The script checks if an image for the latest headline exists in `images/`.
3. If the image exists, it skips the generation; otherwise, it generates the image using OpenAI's DALL·E API.
4. The image is resized, and the headline is added.
5. Finally, the image is displayed on the Inky Impression.

## **Project Structure**

```
frame/
│
├── display_on_inky.py          # Handles displaying the image on the Inky Impression
├── image_generation.py         # Handles OpenAI DALL·E API image generation
├── image_io.py                 # Handles downloading and saving images
├── image_processing.py         # Handles resizing and cropping images
├── text_processing.py          # Handles text wrapping and adding titles to images
├── rss_feed.py                 # Fetches the latest headlines from an RSS feed
├── utils.py                    # Utility functions (e.g., generating filenames)
├── config.py                   # Configuration settings (image size, padding, etc.)
├── requirements.txt            # Python dependencies
├── .env                        # Stores environment variables like OPENAI_API_KEY
├── README.md                   # Project documentation
├── main.py                     # Main script that coordinates everything
└── images/                     # Directory to store generated images
```

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
