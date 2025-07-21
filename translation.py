# translation.py
# This module handles the text translation logic using the deep-translator library.

from deep_translator import GoogleTranslator

def translate_text(text, dest_lang='en'):
    """
    Translates a given text to the destination language.

    Args:
        text (str): The text to translate.
        dest_lang (str): The destination language code (e.g., 'en' for English).

    Returns:
        str: The translated text, or the original text if translation fails.
    """
    if not text.strip():
        return ""
        
    try:
        # The deep-translator library automatically detects the source language.
        translated_text = GoogleTranslator(source='auto', target=dest_lang).translate(text)
        return translated_text
    except Exception as e:
        print(f"Translation failed: {e}")
        # Return the original text if translation fails
        return text
