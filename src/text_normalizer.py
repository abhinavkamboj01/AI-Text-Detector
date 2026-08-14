import re


class TextNormalizer:
    """
    Normalizes text extracted from PDFs.

    Responsibilities:
    - Remove extra whitespace
    - Fix line-break artifacts
    - Remove repeated punctuation
    - Normalize quotes and dashes
    - Remove invisible characters
    - Normalize spacing around punctuation

    NOTE:
    This class intentionally DOES NOT guess missing spaces
    between words (e.g. "internationalparticipation"),
    because doing so reliably requires a dictionary-based or
    language-model-based approach.
    """

    def __init__(self):
        pass

    # ---------------------------------------------------------
    # Main API
    # ---------------------------------------------------------

    def normalize(self, text: str) -> str:

        if not text:
            return ""

        text = self.remove_invisible_characters(text)
        text = self.normalize_quotes(text)
        text = self.normalize_dashes(text)
        text = self.normalize_whitespace(text)
        text = self.normalize_punctuation_spacing(text)
        text = self.remove_repeated_punctuation(text)

        return text.strip()

    # ---------------------------------------------------------
    # Remove invisible unicode characters
    # ---------------------------------------------------------

    def remove_invisible_characters(self, text):

        invisible = [
            "\u200b",
            "\u200c",
            "\u200d",
            "\ufeff",
            "\xa0"
        ]

        for ch in invisible:
            text = text.replace(ch, " ")

        return text

    # ---------------------------------------------------------
    # Normalize whitespace
    # ---------------------------------------------------------

    def normalize_whitespace(self, text):

        text = text.replace("\n", " ")
        text = text.replace("\r", " ")
        text = text.replace("\t", " ")

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    # ---------------------------------------------------------
    # Normalize quotes
    # ---------------------------------------------------------

    def normalize_quotes(self, text):

        replacements = {

            "“": '"',
            "”": '"',
            "‘": "'",
            "’": "'"

        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        return text

    # ---------------------------------------------------------
    # Normalize dashes
    # ---------------------------------------------------------

    def normalize_dashes(self, text):

        replacements = {

            "–": "-",
            "—": "-",
            "−": "-"

        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        return text

    # ---------------------------------------------------------
    # Normalize punctuation spacing
    # ---------------------------------------------------------

    def normalize_punctuation_spacing(self, text):

        text = re.sub(r"\s+([.,!?;:])", r"\1", text)
        text = re.sub(r"([.,!?;:])([A-Za-z])", r"\1 \2", text)

        return text

    # ---------------------------------------------------------
    # Remove repeated punctuation
    # ---------------------------------------------------------

    def remove_repeated_punctuation(self, text):

        text = re.sub(r"\.{2,}", ".", text)
        text = re.sub(r",{2,}", ",", text)
        text = re.sub(r"!{2,}", "!", text)
        text = re.sub(r"\?{2,}", "?", text)

        return text