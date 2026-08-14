from src.inference.pdf_reader import PDFReader
from src.cleaner import Cleaner
from src.inference.turnitin_filter import TurnitinFilter
from src.text_normalizer import TextNormalizer
from src.inference.chunk_builder import ChunkBuilder
from src.inference.predictor import Predictor


class Detector:
    """
    Complete AI Detection Pipeline

    PDF
        ↓
    PDFReader
        ↓
    Cleaner
        ↓
    TurnitinFilter
        ↓
    TextNormalizer
        ↓
    ChunkBuilder
        ↓
    ModernBERT Predictor
        ↓
    Results
    """

    def __init__(self):

        self.cleaner = Cleaner()
        self.turnitin_filter = TurnitinFilter()
        self.normalizer = TextNormalizer()
        self.chunk_builder = ChunkBuilder()
        self.predictor = Predictor()

    # ---------------------------------------------------------

    def detect(self, pdf_path):

        # -----------------------------------------------------
        # Read PDF
        # -----------------------------------------------------

        reader = PDFReader(pdf_path)

        spans = reader.extract()

        reader.close()

        print(f"Original Spans  : {len(spans)}")

        # -----------------------------------------------------
        # Cleaner
        # -----------------------------------------------------

        spans = self.cleaner.process(spans)

        print(f"Clean Spans     : {len(spans)}")

        # -----------------------------------------------------
        # Turnitin Filter
        # -----------------------------------------------------

        spans = self.turnitin_filter.process(spans)

        print(f"Filtered Spans  : {len(spans)}")

        # -----------------------------------------------------
        # Normalize Text
        # -----------------------------------------------------

        normalized = []

        for span in spans:

            text = self.normalizer.normalize(
                span["text"]
            )

            if not text:
                continue

            span["text"] = text

            normalized.append(span)

        spans = normalized

        print(f"Normalized      : {len(spans)}")

        # -----------------------------------------------------
        # Build Chunks
        # -----------------------------------------------------

        chunks = self.chunk_builder.build(spans)

        print(f"Chunks          : {len(chunks)}")

        if not chunks:
            print("No chunks found.")
            return []

        # -----------------------------------------------------
        # Batch Prediction
        # -----------------------------------------------------

        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        predictions = self.predictor.predict_batch(
            texts=texts,
            batch_size=32
        )

        # -----------------------------------------------------
        # Merge Results
        # -----------------------------------------------------

        results = []

        for chunk, prediction in zip(chunks, predictions):

            results.append({

                "page": chunk["page"],

                # list of original span bounding boxes
                "bboxes": chunk["bboxes"],

                "text": chunk["text"],

                "word_count": chunk["word_count"],

                "label": prediction["label"],

                "confidence": prediction["confidence"],

                "human_probability":
                    prediction["human_probability"],

                "ai_probability":
                    prediction["ai_probability"]

            })

        return results