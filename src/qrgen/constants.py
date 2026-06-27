from pathlib import Path

ASSETS_DIR = Path(__file__).parent / "gui" / "assets"
ASSETS_DIR.mkdir(exist_ok=True)

GENERATED_DIR = Path.home() / "Documents" / "qrgen"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)
