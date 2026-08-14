import re


class Cleaner:
    """
    Cleans raw PDF text spans before matching.

    Removes:
    - Empty spans
    - First page (already skipped by PDFReader)
    - URLs
    - Turnitin IDs
    - Submission IDs
    - AI Writing Submission headers
    - Page X of Y
    - Standalone page numbers
    - Headers / Footers
    """

    def __init__(self):

        # -----------------------------
        # Remove URLs
        # -----------------------------

        self.url_pattern = re.compile(
            r"https?://\S+|www\.\S+",
            re.IGNORECASE
        )

        # -----------------------------
        # Turnitin object IDs
        # -----------------------------

        self.turnitin_pattern = re.compile(
            r"trn:oid:::[^\s]+",
            re.IGNORECASE
        )

        # -----------------------------
        # Page numbers
        # -----------------------------

        self.page_pattern = re.compile(
            r"Page\s+\d+\s+of\s+\d+",
            re.IGNORECASE
        )

        # -----------------------------
        # Submission ID
        # -----------------------------

        self.submission_pattern = re.compile(
            r"Submission\s+ID",
            re.IGNORECASE
        )

        # -----------------------------
        # AI Writing Submission
        # -----------------------------

        self.ai_submission_pattern = re.compile(
            r"AI\s+Writing\s+Submission",
            re.IGNORECASE
        )

        # -----------------------------
        # Standalone numbers
        # -----------------------------

        self.number_pattern = re.compile(
            r"^\d+$"
        )

    # ---------------------------------------------------------

    def clean_text(self, text):

        text = text.strip()

        text = self.url_pattern.sub("", text)

        text = self.turnitin_pattern.sub("", text)

        text = self.page_pattern.sub("", text)

        text = self.submission_pattern.sub("", text)

        text = self.ai_submission_pattern.sub("", text)

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    # ---------------------------------------------------------

    def should_skip(self, text):

        if not text:
            return True

        if len(text) < 2:
            return True

        if self.number_pattern.fullmatch(text):
            return True

        lower = text.lower()

        # Header/Footer keywords

        blocked = [

            "submission id",
            "page ",
            "ai writing submission",

        ]

        for item in blocked:

            if lower.startswith(item):
                return True

        return False

    # ---------------------------------------------------------

    def process(self, spans):

        cleaned = []

        for span in spans:

            text = self.clean_text(
                span["text"]
            )

            if self.should_skip(text):
                continue

            span["text"] = text

            cleaned.append(span)

        return cleaned