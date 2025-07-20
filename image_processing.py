# image_processing.py
import cv2
import numpy as np

def inpaint_text_area(image, bounding_box):
    """Erases the area defined by a bounding box using inpainting."""
    x, y, w, h = bounding_box
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)
    inpainted_image = cv2.inpaint(image, mask, inpaintRadius=3, flags=cv2.INPAINT_NS)
    return inpainted_image

def draw_translated_text(image, text, bounding_box):
    """Draws the translated text onto the image."""
    x, y, w, h = bounding_box
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    font_color = (0, 0, 0) # Black
    thickness = 1
    text_position = (x, y + int(h/2))
    cv2.putText(image, text, text_position, font, font_scale, font_color, thickness, cv2.LINE_AA)
    return image
