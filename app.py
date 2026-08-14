import os
import tempfile
from pathlib import Path

import streamlit as st

from src.inference.detector import Detector
from src.inference.report_generator import ReportGenerator
from src.inference.pdf_highlighter import PDFHighlighter


# -------------------------------------------------
# Page Config
# -------------------------------------------------

st.set_page_config(
    page_title="Textify: AI Text Detector",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Textify: AI Text Detector")

st.markdown(
    "Detect AI-generated text from PDF documents."
)

st.divider()

# -------------------------------------------------
# Upload
# -------------------------------------------------

uploaded_pdf = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

# -------------------------------------------------

if uploaded_pdf is not None:

    st.success(f"Uploaded: {uploaded_pdf.name}")

    if st.button(
        "🚀 Detect AI",
        use_container_width=True
    ):

        with st.spinner("Running AI Detection..."):

            # -------------------------
            # Save temp PDF
            # -------------------------

            temp_dir = tempfile.mkdtemp()

            pdf_path = os.path.join(
                temp_dir,
                uploaded_pdf.name
            )

            with open(pdf_path, "wb") as f:
                f.write(uploaded_pdf.getbuffer())

            # -------------------------
            # Detector
            # -------------------------

            detector = Detector()

            results = detector.detect(pdf_path)

            # -------------------------
            # Report
            # -------------------------

            report = ReportGenerator()

            summary = report.generate(
                results,
                uploaded_pdf.name
            )

            # -------------------------
            # Highlight PDF
            # -------------------------

            highlighter = PDFHighlighter()

            highlighted_pdf = highlighter.highlight(
                pdf_path,
                results
            )

        st.success("Detection Complete!")

        st.divider()

        # ==========================================================
        # Metrics
        # ==========================================================

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "AI %",
            f"{summary['ai_percentage']:.2f}%"
        )

        c2.metric(
            "Human %",
            f"{summary['human_percentage']:.2f}%"
        )

        c3.metric(
            "Confidence",
            f"{summary['average_confidence']*100:.2f}%"
        )

        st.divider()

        # ==========================================================
        # Page Statistics
        # ==========================================================

        st.subheader("Page-wise AI Detection")

        for page in summary["page_statistics"]:

            st.write(
                f"Page {page['page']}  ({page['ai_percentage']}%)"
            )

            st.progress(
                page["ai_percentage"] / 100
            )

        st.divider()

        # ==========================================================
        # CSV
        # ==========================================================

        csv_path = summary["csv_path"]

        if Path(csv_path).exists():

            with open(csv_path, "rb") as f:

                st.download_button(
                    "📥 Download Predictions CSV",
                    f,
                    file_name="predictions.csv",
                    mime="text/csv",
                    use_container_width=True
                )

        # ==========================================================
        # Highlighted PDF
        # ==========================================================

        if Path(highlighted_pdf).exists():

            with open(highlighted_pdf, "rb") as f:

                st.download_button(
                    "📄 Download Highlighted PDF",
                    f,
                    file_name=Path(highlighted_pdf).name,
                    mime="application/pdf",
                    use_container_width=True
                )