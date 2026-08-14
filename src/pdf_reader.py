import fitz
from pathlib import Path


class PDFReader:
    """
    Reads PDF documents and extracts text spans with metadata.

    NOTE:
    - Skips the first page (cover page).
    - Does NOT perform any cleaning.
    - Does NOT detect highlights.
    - Does NOT split sentences.
    """

    def __init__(self, pdf_path: str):

        self.pdf_path = Path(pdf_path)

        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {self.pdf_path}")

        self.document = fitz.open(self.pdf_path)

    def get_total_pages(self):
        return len(self.document)

    def extract(self):

        spans_data = []

        # Start from page 2 (skip cover page)
        for page_number in range(1, len(self.document)):

            page = self.document[page_number]

            page_dict = page.get_text("dict")

            for block_index, block in enumerate(page_dict["blocks"]):

                # Ignore images
                if block["type"] != 0:
                    continue

                for line_index, line in enumerate(block["lines"]):

                    for span_index, span in enumerate(line["spans"]):

                        text = span["text"].strip()

                        if not text:
                            continue

                        spans_data.append(
                            {
                                "pdf_name": self.pdf_path.name,
                                "page": page_number + 1,
                                "block": block_index,
                                "line": line_index,
                                "span": span_index,
                                "text": text,
                                "bbox": span["bbox"],
                                "font": span["font"],
                                "size": span["size"],
                                "color": span["color"],
                                "flags": span["flags"]
                            }
                        )

        return spans_data

    def close(self):
        self.document.close()