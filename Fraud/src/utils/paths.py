from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[2]  # project root (where app.py lives)

def asset_path(*parts) -> Path:
    return BASE_DIR / "assets" / Path(*parts)
