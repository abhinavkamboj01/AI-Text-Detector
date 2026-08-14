from pathlib import Path

from src.inference.detector import Detector
from src.inference.report_generator import ReportGenerator
from src.inference.pdf_highlighter import PDFHighlighter


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

PDF_PATH = "input/sample.pdf"


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    pdf_path = Path(PDF_PATH)

    if not pdf_path.exists():
        print(f"PDF not found: {pdf_path}")
        return

    print("\n" + "=" * 80)
    print("AI TEXT DETECTOR")
    print("=" * 80)

    # -----------------------------------------------------
    # Detection
    # -----------------------------------------------------

    detector = Detector()

    results = detector.detect(str(pdf_path))

    if not results:
        print("No predictions generated.")
        return

    # -----------------------------------------------------
    # Report
    # -----------------------------------------------------

    report = ReportGenerator()

    summary = report.generate(
        results,
        document_name=pdf_path.name
    )

    # -----------------------------------------------------
    # Highlight PDF
    # -----------------------------------------------------

    highlighter = PDFHighlighter()

    highlighted_pdf = highlighter.highlight(
        pdf_path=str(pdf_path),
        predictions=results
    )

    # -----------------------------------------------------
    # Final Summary
    # -----------------------------------------------------

    print("\n" + "=" * 80)
    print("FINAL SUMMARY")
    print("=" * 80)

    print(f"Document           : {summary['document']}")
    print(f"AI Percentage      : {summary['ai_percentage']:.2f}%")
    print(f"Human Percentage   : {summary['human_percentage']:.2f}%")
    print(f"Average Confidence : {summary['average_confidence']:.4f}")

    print(f"\nPredictions CSV    : {summary['csv_path']}")
    print(f"Highlighted PDF    : {highlighted_pdf}")

    print("=" * 80)


# ---------------------------------------------------------

if __name__ == "__main__":
    main()