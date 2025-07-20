# translation.py
from googletrans import Translator

def translate_text(text, dest_lang='en'):
    """Translates a given text to the destination language."""
    if not text.strip():
        return ""
    try:
        translator = Translator()
        translation_result = translator.translate(text, dest=dest_lang)
        return translation_result.text
    except Exception as e:
        print(f"Translation failed: {e}")
        return text
