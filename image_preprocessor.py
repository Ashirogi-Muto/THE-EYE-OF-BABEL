# image_preprocessor.py
# This module contains functions to pre-process images for better OCR accuracy.

import cv2

def preprocess_for_ocr(image):
    """
    Applies pre-processing steps to an image to improve OCR results,
    based on common best practices.

    Args:
        image: The source OpenCV image (in BGR color format).

    Returns:
        A new, pre-processed image ready for OCR.
    """
    # 1. Convert the image to grayscale. This is a standard first step.
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 2. Apply a median blur to remove salt-and-pepper noise.
    #    This is a key step recommended for cleaning up images before OCR.
    #    The kernel size (e.g., 3 or 5) determines how much to blur. A small
    #    kernel is usually best to avoid blurring the text itself.
    gray_image = cv2.medianBlur(gray_image, 3)

    # 3. Apply a global threshold to get a pure black-and-white image.
    #    cv2.THRESH_OTSU automatically determines the best threshold value.
    _, processed_image = cv2.threshold(
        gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU
    )

    return processed_image
