import pymupdf


class PDFReader:
    """
    Reads a normal PDF for inference.

    Returns text spans with:
        - page
        - bbox
        - text

    Unlike the training PDFReader, this one:
        ✓ Doesn't use labels
        ✓ Doesn't use highlights
        ✓ Doesn't use confidence
    """

    def __init__(self, pdf_path: str):

        self.document = pymupdf.open(pdf_path)

    # ---------------------------------------------------------
    # Close PDF
    # ---------------------------------------------------------

    def close(self):

        self.document.close()

    # ---------------------------------------------------------
    # Extract text spans
    # ---------------------------------------------------------

    def extract(self):

        spans = []

        for page_number, page in enumerate(self.document):

            text_dict = page.get_text("dict")

            for block in text_dict.get("blocks", []):

                if block.get("type") != 0:
                    continue

                for line in block.get("lines", []):

                    for span in line.get("spans", []):

                        text = span.get("text", "").strip()

                        if not text:
                            continue

                        spans.append(
                            {
                                "page": page_number + 1,
                                "bbox": span["bbox"],
                                "text": text,
                            }
                        )

        return spans