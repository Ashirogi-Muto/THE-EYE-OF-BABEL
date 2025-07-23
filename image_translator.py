# image_translator.py
# This module contains the core orchestration logic for translating a single image.

import cv2
import os
import text_detection
import image_processing
import translation
# We no longer need the preprocessor for PaddleOCR
# import image_preprocessor 
from config import OUTPUT_FOLDER

def process_image(image_path):
    """Orchestrates the translation process for a single image file."""
    print(f"Starting to process image: {image_path}")

    try:
        original_image = cv2.imread(image_path)
        if original_image is None:
            print(f"Error: Could not load image at path: {image_path}")
            return False
    except Exception as e:
        print(f"Error loading image: {e}")
        return False

    # --- Text Detection ---
    # NOTE: We pass the original image to PaddleOCR. Pre-processing is not
    # needed and can harm the accuracy of deep learning models.
    print("Detecting text...")
    raw_text_data = text_detection.get_text_data(original_image)
    
    print("Grouping words into lines...")
    grouped_lines = text_detection.group_text_by_lines(raw_text_data)
    print(f"Found {len(grouped_lines)} lines to process.")

    if not grouped_lines:
        print("No text detected. Skipping image modification.")
        # Even if no text is found, we'll save a copy of the original for consistency.
        base_filename = os.path.basename(image_path)
        original_output_path = os.path.join(OUTPUT_FOLDER, "original", base_filename)
        cv2.imwrite(original_output_path, original_image)
        return False # Exit if no text is found

    # --- Image Modification ---
    # Create a copy of the original color image to draw on.
    processing_image = original_image.copy()

    # --- TWO-LOOP LOGIC ---
    # Loop 1: Erase all text areas first to create a clean slate.
    print("Erasing original text...")
    for line in grouped_lines:
        x, y, w, h = line['box']
        processing_image = image_processing.inpaint_text_area(processing_image, (x, y, w, h))

    # Loop 2: Translate and draw the new text onto the clean image.
    print("Drawing translated text...")
    for line in grouped_lines:
        line_text = line['text']
        x, y, w, h = line['box']
        
        translated_text = translation.translate_text(line_text)
        processing_image = image_processing.draw_translated_text(processing_image, translated_text, (x, y, w, h))

    # --- Save and Display Results ---
    print("Processing complete. Saving results...")
    
    base_filename = os.path.basename(image_path)
    original_output_path = os.path.join(OUTPUT_FOLDER, "original", base_filename)
    translated_output_path = os.path.join(OUTPUT_FOLDER, "translated", base_filename)

    cv2.imwrite(original_output_path, original_image)
    save_success = cv2.imwrite(translated_output_path, processing_image)
    
    if save_success:
        print(f"Translated image saved to: {translated_output_path}")
    else:
        print(f"Error: Failed to save translated image.")

    cv2.imshow('Original Image', original_image)
    cv2.imshow('Translated Image', processing_image)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()
    return True
