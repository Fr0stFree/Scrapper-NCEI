import datetime as dt
from pathlib import Path
from typing import Final


BASE_DIR: Final[Path] = Path(__file__).parent.parent
START_DATE: Final[dt.date] = dt.datetime.now().date()
END_DATE: Final[dt.date] = START_DATE - dt.timedelta(days=4)
BASE_URL: Final[str] = f'https://www.ncei.noaa.gov/data/global-summary-of-the-day/access/{START_DATE.year}/'
