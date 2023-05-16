from pathlib import Path


BASE_DIR: Path = Path(__file__).parent.parent
TEMP_DIR: Path = BASE_DIR / 'temp'
DATA_DIR: Path = BASE_DIR / 'data'
DATA_AMOUNT_IN_DAYS: int = 30

if not TEMP_DIR.exists():
    TEMP_DIR.mkdir()

if not DATA_DIR.exists():
    DATA_DIR.mkdir()
