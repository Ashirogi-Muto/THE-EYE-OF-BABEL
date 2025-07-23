# The Eye of Babel

An advanced Python application that performs in-place translation of text on images. The script detects text, erases it by inpainting the background, translates the text, and then intelligently draws the translated text back onto the image.

## Features
- **Folder Watching:** Automatically processes new images dropped into an `input_images` folder.
- **Modular Codebase:** Organized into separate modules for configuration, text detection, image processing, and translation.
- **Advanced OCR:** Uses PaddleOCR for robust multilingual text detection.
- **Inpainting:** Intelligently erases original text from the image by filling the area with the surrounding color.
- **In-Place Translation:** Draws the translated text back onto the image.

## How to Use
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR-USERNAME/The-Eye-of-Babel.git](https://github.com/YOUR-USERNAME/The-Eye-of-Babel.git)
    cd The-Eye-of-Babel
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the script:**
    ```bash
    python main.py
    ```
4.  Drop an image file into the `input_images` folder and check the `output` folder for the result.