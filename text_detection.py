# text_detection.py
# This module is responsible for detecting text and its properties in an image.

import numpy as np
import cv2
from paddleocr import PaddleOCR

# --- Model Initialization ---
# This loads the PaddleOCR model into memory.
# It's done once when the module is first imported for efficiency.
# The first time this runs, it will download the necessary model weights.
# We use lang='ch' to load the robust multilingual model which supports
# Chinese, English, and many other languages.
print("Loading multilingual PaddleOCR model... (This may take a moment on first run)")
ocr_model = PaddleOCR(use_angle_cls=True, lang='ch')
print("PaddleOCR model loaded.")


def get_text_data(image):
    """Performs OCR and returns the raw result list."""
    result = ocr_model.ocr(image)
    return result


def group_text_by_lines(ocr_result):
    """Takes the raw PaddleOCR result and formats it for our application."""
    # Check for empty or invalid results
    if not ocr_result or not ocr_result[0]:
        return []

    # The result for a single image is a list containing one item.
    result_page = ocr_result[0]
    if not result_page:
        return []

    grouped_data = []
    
    # Handle the dictionary-based format from newer PaddleOCR versions
    if isinstance(result_page, dict):
        try:
            boxes = result_page.get('rec_polys', [])
            texts = result_page.get('rec_texts', [])
            for box, text in zip(boxes, texts):
                points = np.array(box, dtype=np.int32)
                x, y, w, h = cv2.boundingRect(points)
                grouped_data.append({'text': text, 'box': (x, y, w, h)})
            return grouped_data
        except Exception as e:
            print(f"Error parsing PaddleOCR dictionary result: {e}")
            return []
    
    # Handle the standard list-of-lists format as a fallback for older versions
    try:
        for line in result_page:
            points = np.array(line[0], dtype=np.int32)
            x, y, w, h = cv2.boundingRect(points)
            text, confidence = line[1]
            grouped_data.append({'text': text, 'box': (x, y, w, h)})
    except Exception as e:
        print(f"Error parsing PaddleOCR list result: {e}")
        return []

    return grouped_data
