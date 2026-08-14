from pathlib import Path
import pymupdf


class PDFHighlighter:
    """
    Highlights AI-generated text in a PDF.

    Colors:
        Red    -> AI Probability >= 0.90
        Orange -> AI Probability >= 0.75
        Yellow -> AI Probability >= 0.50
    """

    def __init__(
        self,
        red_threshold=0.90,
        orange_threshold=0.75,
        yellow_threshold=0.50,
    ):

        self.red_threshold = red_threshold
        self.orange_threshold = orange_threshold
        self.yellow_threshold = yellow_threshold

    # ---------------------------------------------------------

    def get_color(self, probability):

        if probability >= self.red_threshold:
            return (1, 0, 0)  # Red

        elif probability >= self.orange_threshold:
            return (1, 0.5, 0)  # Orange

        elif probability >= self.yellow_threshold:
            return (1, 1, 0)  # Yellow

        return None

    # ---------------------------------------------------------

    def highlight(
        self,
        pdf_path,
        predictions,
        output_path=None
    ):

        document = pymupdf.open(pdf_path)

        total_highlights = 0

        for prediction in predictions:

            probability = prediction["ai_probability"]

            color = self.get_color(probability)

            if color is None:
                continue

            page_number = prediction["page"] - 1

            page = document[page_number]

            for bbox in prediction["bboxes"]:

                rect = pymupdf.Rect(bbox)

                annotation = page.add_highlight_annot(rect)

                annotation.set_colors(stroke=color)

                annotation.update()

                total_highlights += 1

        # -----------------------------------------------------

        if output_path is None:

            pdf_name = Path(pdf_path).stem

            output_path = (
                Path("output") /
                f"{pdf_name}_highlighted.pdf"
            )

        Path(output_path).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        document.save(
            str(output_path),
            garbage=4,
            deflate=True
        )

        document.close()

        print()

        print("=" * 60)

        print("PDF Highlighting Complete")

        print("=" * 60)

        print(f"Highlights Added : {total_highlights}")

        print(f"Saved To         : {output_path}")

        print("=" * 60)

        return str(output_path)