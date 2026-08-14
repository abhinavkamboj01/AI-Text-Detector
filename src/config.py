from pathlib import Path

# ======================================================
# Project Paths
# ======================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

PDF_FOLDER = DATA_DIR / "pdfs"

RENDERED_PAGES = DATA_DIR / "rendered_pages"

RAW_DATA = DATA_DIR / "raw"

PROCESSED_DATA = DATA_DIR / "processed"

OUTPUT_DIR = BASE_DIR / "output"

DEBUG_DIR = DATA_DIR / "debug_crops"

# ======================================================
# PDF Rendering
# ======================================================

RENDER_DPI = 300

TEXT_PADDING = 6

# ======================================================
# Highlight Colors (Normalized RGB)
# ======================================================

HIGHLIGHT_COLORS = {

    "AI": [

        (0.320, 0.777, 0.855),

    ],

    "IGNORE": [

        (0.715, 0.547, 0.984),

    ]

}

# Maximum allowed difference between colors
COLOR_TOLERANCE = 0.05

# ======================================================
# Rectangle Matching
# ======================================================

# Minimum overlap between text span and highlight rectangle
OVERLAP_THRESHOLD = 0.55

# ======================================================
# Cleaning Parameters
# ======================================================

MIN_TEXT_LENGTH = 5

REMOVE_NUMBERS = True

REMOVE_URLS = True

REMOVE_FOOTERS = True

REMOVE_EMPTY_TEXT = True

# ======================================================
# Dataset
# ======================================================

RAW_DATASET = OUTPUT_DIR / "raw_dataset.csv"

FINAL_DATASET = OUTPUT_DIR / "final_dataset.csv"

# ======================================================
# Debug
# ======================================================

DEBUG = True

SHOW_FIRST_RESULTS = 10