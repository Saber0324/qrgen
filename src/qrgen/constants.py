from pathlib import Path

ASSETS_DIR = Path(__file__).parent / "gui" / "assets"
ASSETS_DIR.mkdir(exist_ok=True)

GENERATED_DIR = Path(__file__).parent / "generated"
GENERATED_DIR.mkdir(exist_ok=True)
