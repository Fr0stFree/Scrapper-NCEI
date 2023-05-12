import asyncio
import datetime as dt
from pathlib import Path
from typing import Final

from src import DataProcessor, Manipulator, PageDownloader, PageParser

BASE_DIR: Final[Path] = Path(__file__).parent
START_DATE: Final[dt.date] = dt.datetime.now().date()
END_DATE: Final[dt.date] = START_DATE - dt.timedelta(days=4)
BASE_URL: Final[str] = f'https://www.ncei.noaa.gov/data/global-summary-of-the-day/access/{START_DATE.year}/'


async def main() -> None:
    station_ids = Manipulator.load_stations(BASE_DIR / 'stations.txt')

    page = await PageDownloader.get(BASE_URL)
    urls = (f'{BASE_URL}{link}' for link in PageParser.parse(station_ids, page))
    async for csv_file in PageDownloader.get_concurrently(urls):
        DataProcessor.run(csv_file, start_date=START_DATE, end_date=END_DATE)

    Manipulator.save_geojson(data=DataProcessor.result, path=BASE_DIR / 'data')


if __name__ == "__main__":
    asyncio.run(main())
