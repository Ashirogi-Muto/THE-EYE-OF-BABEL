# text_detection.py
# This module is responsible for detecting text and its properties in an image.

import pytesseract
import pandas as pd
from config import TESSERACT_PATH

# Configure pytesseract
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def get_text_data(image):
    """
    Performs OCR on an image and returns detailed data about each detected word.
    This is our low-level function that gets raw data from Tesseract.

    Args:
        image: An OpenCV image object (as a NumPy array).

    Returns:
        pandas.DataFrame: A DataFrame containing data for each word, including
                          its bounding box, confidence, and text.
    """
    # Use image_to_data to get detailed information including bounding boxes
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    
    df = pd.DataFrame(data)
    
    # Filter out entries with no text or low confidence
    df = df[df.conf != -1]
    df = df.dropna(subset=['text'])
    df = df[df.text.str.strip() != '']

    return df

def group_text_by_lines(df):
    """
    Takes the raw word data and groups it into lines of text.
    This is our high-level function that makes the data more useful.

    Args:
        df (pandas.DataFrame): The DataFrame from get_text_data.

    Returns:
        list: A list of dictionaries, where each dictionary represents a line of text
              and contains the full text and a single bounding box for the entire line.
    """
    # Group the DataFrame by block, paragraph, and line number. This effectively
    # groups all words that belong on the same line.
    line_groups = df.groupby(['block_num', 'par_num', 'line_num'])

    grouped_data = []
    for name, group in line_groups:
        # For each line group, combine the text of all words into a single string.
        line_text = ' '.join(group['text'].astype(str))

        # Now, calculate a single bounding box for the entire line.
        # x_min is the smallest 'left' value in the group.
        x_min = group['left'].min()
        # y_min is the smallest 'top' value in the group.
        y_min = group['top'].min()
        # To get the rightmost edge, we find the max of (left + width).
        x_max = (group['left'] + group['width']).max()
        # To get the bottommost edge, we find the max of (top + height).
        y_max = (group['top'] + group['height']).max()

        # Calculate the overall width and height of the line's bounding box.
        line_width = x_max - x_min
        line_height = y_max - y_min

        # Store the consolidated data for this line.
        grouped_data.append({
            'text': line_text,
            'box': (x_min, y_min, line_width, line_height)
        })
        
    return grouped_data
