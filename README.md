# **Frame**

Frame is a Python project that fetches the latest headlines from an RSS feed, generates images using OpenAI's DALL·E API or Getimg.ai's Stable Diffusion XL, processes the images by adding article titles, and displays them on an Inky Impression e-ink display.

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
sudo apt install libopenblas-dev fonts-roboto nodejs npm
```

- **libopenblas-dev**: Required for numerical computations by libraries like NumPy.
- **fonts-roboto**: Required for adding text in the Roboto font to images.
- **nodejs**: Required for running the frontend React app.
- **npm**: Node.js package manager.

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

4. Set up your OpenAI API and Getimg.ai key by creating a `.env` file in the root of the project:

   ```bash
   touch .env
   ```

   Add the following line to the `.env` file, replacing `your_openai_api_key_here` and `your_getimg_api_key_here` with your actual keys:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   GETIMG_API_KEY=your_getimg_api_key_here
   ```

5. Go to the `web/` directory and install the required Node.js dependencies:

   ```bash
   cd web
   sudo npm install -g pnpm
   pnpm install
   ```

6. Build the React app:

   ```bash
   pnpm build
   ```

Or as a all in once command:

```bash
git clone https://github.com/ckuijjer/frame.git
cd frame
python -m venv env
source env/bin/activate
pip install -r requirements.txt
touch .env
cd web
npm install -g pnpm
pnpm install
pnpm build
```

Just remember to add your API keys to the `.env` file.

## **Configuration**

### **Environment Variables**

Ensure you have the following environment variables set in your `.env` file:

- **`OPENAI_API_KEY`**: Your OpenAI API key to generate images using DALL·E.
- **`GETIMG_API_KEY`**: Your Getimg.ai API key to generate images using Stable Diffusion XL.

### **Default Settings**

- The generated images will be saved in the `images/` directory.
- The RSS feed URL, image sizes, and padding can be configured directly in the code (see `config.py` for image and text settings).

## **Usage**

After installing the dependencies and setting up your environment, you can run the main script to fetch the latest headlines, generate images, and display them on your Inky Impression display:

```bash
python render_news_to_display.py
```

To run the web server and display the React app, run the following commands:

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
- **`main.py`**: Starts the Bottle server, serves the React app, and includes the `/api/render` endpoint for triggering `render_news_to_display`.
- **`config.py`**: Configuration settings such as image sizes, padding, and environment variables.
- **`web/`**: Contains the Vite-created React app’s source code and configurations.
  - **`dist/`**: This folder contains the compiled, production-ready build of the React app (generated by `vite build`). It serves as the source for the static files in `main.py`.
-

### **Example Workflow**

1. Run `python render_news_to_display.py` to fetch the latest headlines.
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
├── images/                     # Directory to store generated images
├── web/                        # Contains the Vite-created React app’s source code and configurations
│   └── dist/                   # Contains the compiled, production-ready build of the React app
```

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## **Acknowledgements**

With help from ChatGPT, see the [ChatGPT conversation](https://chatgpt.com/share/67150e7c-3528-800e-b2a2-3108734eea47) for more information.

```

```
