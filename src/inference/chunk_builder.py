import re


class ChunkBuilder:
    """
    Builds inference chunks while preserving the
    original span bounding boxes.

    Each output chunk contains:
        - page
        - text
        - word_count
        - bboxes (list of span bounding boxes)
    """

    def __init__(
        self,
        max_vertical_gap=25,
        max_words=200,
    ):
        self.max_vertical_gap = max_vertical_gap
        self.max_words = max_words

    # ---------------------------------------------------------

    def should_merge(self, previous, current):

        if previous["page"] != current["page"]:
            return False

        previous_bottom = previous["bbox"][3]
        current_top = current["bbox"][1]

        gap = current_top - previous_bottom

        return gap <= self.max_vertical_gap

    # ---------------------------------------------------------

    def clean_text(self, text):

        text = text.replace("\n", " ")
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    # ---------------------------------------------------------

    def split_chunk(self, chunk):

        words = chunk["text"].split()

        if len(words) <= self.max_words:

            chunk["word_count"] = len(words)

            return [chunk]

        chunks = []

        total_words = len(words)

        start = 0

        while start < total_words:

            end = min(
                start + self.max_words,
                total_words
            )

            piece = {

                "page": chunk["page"],

                "text": " ".join(words[start:end]),

                "word_count": end - start,

                # keep all original bboxes
                "bboxes": chunk["bboxes"]

            }

            chunks.append(piece)

            start = end

        return chunks

    # ---------------------------------------------------------

    def build(self, spans):

        if not spans:
            return []

        chunks = []

        current = {

            "page": spans[0]["page"],

            "text": spans[0]["text"],

            "bbox": spans[0]["bbox"],

            "bboxes": [spans[0]["bbox"]]

        }

        for span in spans[1:]:

            if self.should_merge(current, span):

                current["text"] += " " + span["text"]

                current["bbox"] = (

                    current["bbox"][0],

                    current["bbox"][1],

                    max(
                        current["bbox"][2],
                        span["bbox"][2]
                    ),

                    span["bbox"][3]

                )

                current["bboxes"].append(
                    span["bbox"]
                )

            else:

                current["text"] = self.clean_text(
                    current["text"]
                )

                chunks.extend(
                    self.split_chunk(current)
                )

                current = {

                    "page": span["page"],

                    "text": span["text"],

                    "bbox": span["bbox"],

                    "bboxes": [span["bbox"]]

                }

        current["text"] = self.clean_text(
            current["text"]
        )

        chunks.extend(
            self.split_chunk(current)
        )

        return chunks