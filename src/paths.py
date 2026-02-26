from pathlib import Path

PROJECT_ROOT = Path("/content/drive/MyDrive/Mestrado")

RAW_PATH       = PROJECT_ROOT / "02-datasets" / "01-raw"
PROCESSED_PATH = PROJECT_ROOT / "02-datasets" / "02-processed"
FEATURES_PATH  = PROJECT_ROOT / "02-datasets" / "03-features"
MODELS_PATH    = PROJECT_ROOT / "03-models"
REPORTS_PATH   = PROJECT_ROOT / "04-reports"

def ensure_dirs():
    for p in [RAW_PATH, PROCESSED_PATH, FEATURES_PATH, MODELS_PATH, REPORTS_PATH]:
        p.mkdir(parents=True, exist_ok=True)
