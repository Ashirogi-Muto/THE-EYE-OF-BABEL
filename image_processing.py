# image_processing.py
import cv2
import numpy as np

def inpaint_text_area(image, bounding_box):
    """
    Erases the text area by filling it with the average color of the
    surrounding region, avoiding background bleed.
    """
    x, y, w, h = bounding_box
    
    # --- 1. Define a slightly larger region around the text to sample the color from ---
    # We create a "frame" around the text box to get the sign's color.
    sample_margin = 5  # How many pixels wide the frame should be
    
    # Ensure the sampling area does not go outside the image boundaries
    top = max(0, y - sample_margin)
    bottom = min(image.shape[0], y + h + sample_margin)
    left = max(0, x - sample_margin)
    right = min(image.shape[1], x + w + sample_margin)

    # --- 2. Create a mask to isolate the sampling frame ---
    # This mask will have the text area blacked out, so we only sample the frame.
    frame_mask = np.zeros(image.shape[:2], dtype=np.uint8)
    # Draw the larger frame area in white
    frame_mask[top:bottom, left:right] = 255
    # Black out the actual text area inside the frame
    frame_mask[y:y+h, x:x+w] = 0

    # --- 3. Calculate the average color of the frame ---
    # cv2.mean calculates the average B, G, R, and Alpha values for the masked area.
    # We only need the B, G, R values.
    avg_color = cv2.mean(image, mask=frame_mask)[:3]
    
    # Convert the average color values to integers
    avg_color_int = (int(avg_color[0]), int(avg_color[1]), int(avg_color[2]))

    # --- 4. Fill the text area with the calculated average color ---
    # We draw a solid, filled rectangle over the original text.
    cv2.rectangle(image, (x, y), (x + w, y + h), avg_color_int, -1)
    
    return image

def draw_translated_text(image, text, bounding_box):
    """Draws the translated text onto the image (simple version)."""
    x, y, w, h = bounding_box
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    font_color = (0, 0, 0) # Black
    thickness = 1
    text_position = (x, y + int(h/2)) # Simple vertical centering
    cv2.putText(image, text, text_position, font, font_scale, font_color, thickness, cv2.LINE_AA)
    return image
