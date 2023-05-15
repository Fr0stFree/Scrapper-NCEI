from pathlib import Path


BASE_DIR: Path = Path(__file__).parent.parent
TEMP_DIR: Path = BASE_DIR / 'temp'
DATA_DIR: Path = BASE_DIR / 'data'
DATA_AMOUNT_IN_DAYS: int = 30
