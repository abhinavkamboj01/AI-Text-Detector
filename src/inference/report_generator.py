from pathlib import Path
import pandas as pd


class ReportGenerator:
    """
    Generates the final AI detection report.

    Responsibilities:
    - Compute AI/Human percentages
    - Compute page-wise AI percentages
    - Save predictions.csv
    - Print console report
    """

    def __init__(self, output_dir="output"):

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    # ---------------------------------------------------------

    def generate(
        self,
        results,
        document_name="document.pdf"
    ):

        if not results:
            print("No predictions found.")
            return None

        df = pd.DataFrame(results)

        # -----------------------------------------------------
        # Document Statistics
        # -----------------------------------------------------

        total_chunks = len(df)

        total_words = int(
            df["word_count"].sum()
        )

        ai_weight = (
            df["word_count"] *
            df["ai_probability"]
        ).sum()

        human_weight = (
            df["word_count"] *
            df["human_probability"]
        ).sum()

        ai_percentage = (
            ai_weight /
            total_words
        ) * 100

        human_percentage = (
            human_weight /
            total_words
        ) * 100

        average_confidence = float(
            df["confidence"].mean()
        )

        max_confidence = float(
            df["confidence"].max()
        )

        # -----------------------------------------------------
        # Page Statistics
        # -----------------------------------------------------

        page_statistics = []

        for page in sorted(df["page"].unique()):

            page_df = df[
                df["page"] == page
            ]

            page_words = int(
                page_df["word_count"].sum()
            )

            page_ai = (
                page_df["word_count"] *
                page_df["ai_probability"]
            ).sum()

            page_percentage = (
                page_ai /
                page_words
            ) * 100

            page_statistics.append({

                "page": int(page),

                "words": page_words,

                "ai_percentage":
                    round(
                        page_percentage,
                        2
                    )

            })

        # -----------------------------------------------------
        # Save CSV
        # -----------------------------------------------------

        csv_path = (
            self.output_dir /
            "predictions.csv"
        )

        df.to_csv(
            csv_path,
            index=False
        )

        # -----------------------------------------------------
        # Print Report
        # -----------------------------------------------------

        print()

        print("=" * 70)

        print("AI DETECTION REPORT")

        print("=" * 70)

        print()

        print(f"Document              : {document_name}")

        print(f"Total Chunks          : {total_chunks}")

        print(f"Total Words           : {total_words}")

        print()

        print(f"AI Percentage         : {ai_percentage:.2f}%")

        print(f"Human Percentage      : {human_percentage:.2f}%")

        print()

        print(
            f"Average Confidence    : "
            f"{average_confidence:.4f}"
        )

        print(
            f"Maximum Confidence    : "
            f"{max_confidence:.4f}"
        )

        print()

        print("-" * 70)

        print("Page-wise AI Percentage")

        print("-" * 70)

        for page in page_statistics:

            print(

                f"Page {page['page']:>3}"

                f" : "

                f"{page['ai_percentage']:>6.2f}%"

            )

        print()

        print(f"Predictions CSV Saved : {csv_path}")

        print()

        print("=" * 70)

        # -----------------------------------------------------

        return {

            "document": document_name,

            "total_chunks": total_chunks,

            "total_words": total_words,

            "ai_percentage": round(
                ai_percentage,
                2
            ),

            "human_percentage": round(
                human_percentage,
                2
            ),

            "average_confidence": round(
                average_confidence,
                4
            ),

            "maximum_confidence": round(
                max_confidence,
                4
            ),

            "page_statistics":
                page_statistics,

            "csv_path":
                str(csv_path)

        }