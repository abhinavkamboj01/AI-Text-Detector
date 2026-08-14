import re


class TurnitinFilter:
    """
    Removes Turnitin interface text before AI detection.

    Keeps only the student's actual document.

    Works after Cleaner().
    """

    def __init__(self):

        # ---------------------------------------------------
        # Exact phrases
        # ---------------------------------------------------

        self.blocked_phrases = {

            "quick submit",
            "document details",
            "submission date",
            "download date",
            "file name",
            "file size",
            "cover page",
            "ai writing submission",
            "review required",
            "learn more",
            "turnitin",
            "detected as ai",
            "likely ai-generated",
            "likely ai-paraphrased",
            "characters",
            "words",
            "pages",

        }

        # ---------------------------------------------------
        # Regular expressions
        # ---------------------------------------------------

        self.patterns = [

            re.compile(r"page\s+\d+\s+of\s+\d+", re.I),

            re.compile(r"\d+%\s+detected\s+as\s+ai", re.I),

            re.compile(r"submission\s+id", re.I),

            re.compile(r"download\s+date", re.I),

            re.compile(r"file\s+name", re.I),

            re.compile(r"file\s+size", re.I),

            re.compile(r"\d+\s+characters", re.I),

            re.compile(r"\d+\s+words", re.I),

            re.compile(r"\d+\s+pages", re.I),

            re.compile(r"review\s+required", re.I),

            re.compile(r"learn\s+more", re.I),

        ]

    # -------------------------------------------------------

    def should_remove(self, text):

        if not text:
            return True

        lower = text.lower().strip()

        # exact phrase

        if lower in self.blocked_phrases:
            return True

        # contains phrase

        for phrase in self.blocked_phrases:

            if phrase in lower:
                return True

        # regex

        for pattern in self.patterns:

            if pattern.search(text):
                return True

        return False

    # -------------------------------------------------------

    def process(self, spans):

        filtered = []

        removed = 0

        for span in spans:

            if self.should_remove(span["text"]):

                removed += 1
                continue

            filtered.append(span)

        print(f"Turnitin Removed : {removed}")

        return filtered