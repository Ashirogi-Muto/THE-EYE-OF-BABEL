# file_watcher.py
# This module handles watching a folder for new files to process.

import os
import time
from config import INPUT_FOLDER, PROCESSED_FOLDER, OUTPUT_FOLDER
from image_translator import process_image

def setup_folders():
    """Creates the necessary input, processed, and output folders."""
    os.makedirs(INPUT_FOLDER, exist_ok=True)
    os.makedirs(PROCESSED_FOLDER, exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_FOLDER, "original"), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_FOLDER, "translated"), exist_ok=True)

def watch_folder():
    """Continuously checks the input folder and processes new files."""
    print("--- The Eye of Babel ---")
    print(f"Watching for images in: '{INPUT_FOLDER}'")
    print("Press Ctrl+C to stop.")
    print("-" * 26)
    
    while True:
        try:
            files = [f for f in os.listdir(INPUT_FOLDER) if os.path.isfile(os.path.join(INPUT_FOLDER, f))]
            
            if files:
                filename = files[0]
                input_path = os.path.join(INPUT_FOLDER, filename)
                
                process_image(input_path)

                processed_path = os.path.join(PROCESSED_FOLDER, filename)
                
                # --- FIXED LOGIC ---
                # Use os.replace() instead of os.rename(). os.replace() will
                # overwrite the destination file if it already exists.
                os.replace(input_path, processed_path)
                
                print(f"Moved original file to: '{processed_path}'")
                print("-" * 26)

            time.sleep(5)
            
        except FileNotFoundError:
            print(f"Error: Input folder '{INPUT_FOLDER}' not found. Please create it and restart.")
            time.sleep(5)
