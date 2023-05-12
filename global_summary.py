import asyncio
import datetime as dt
import io
from pathlib import Path
from typing import Iterator, AsyncGenerator, Generator, Final, Set

import aiofiles
import aiohttp
import geojson
import pandas as pd
from bs4 import BeautifulSoup

BASE_DIR: Final[Path] = Path(__file__).parent
BASE_URL: Final[str] = 'https://www.ncei.noaa.gov/data/global-summary-of-the-day/access/'
SEMAPHORE_LIMIT:  Final[int] = 5
with open(BASE_DIR / 'stations.txt') as f:
    STATIONS_IDS: Final[Set] = set([station_id for station_id in f.read().split()])


def parse_page_to_links(html: str) -> Generator[str, None, None]:
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    return (link["href"] for link in table.find_all("a"))


def filter_links(links: Generator[str, None, None]) -> Iterator[str]:
    return filter(lambda link: any([link.startswith(station_id) for station_id in STATIONS_IDS]), links)


async def download_csv(link: str, session: aiohttp.ClientSession,
                       semaphore: asyncio.Semaphore) -> str:
    async with semaphore:
        async with session.get(link) as response:
            response.raise_for_status()
            return await response.text(encoding="utf-8")


async def bulk_download_csv(links: Iterator[str], page_url: str,
                            session: aiohttp.ClientSession) -> AsyncGenerator[str, None]:
    semaphore = asyncio.Semaphore(SEMAPHORE_LIMIT)
    tasks = [asyncio.create_task(download_csv(f'{page_url}{link}', session, semaphore)) for link in links]
    for task in asyncio.as_completed(tasks):
        try:
            csv_file: str = await task
        except Exception:
            continue
        else:
            yield csv_file


def find_rows_by_date(csv_file: str, start: dt.datetime, end: dt.datetime) -> pd.DataFrame:
    df = pd.read_csv(io.StringIO(csv_file), sep=',', header=0)
    rows = df.loc[(df['DATE'] >= start.strftime("%Y-%m-%d")) & (df['DATE'] <= end.strftime("%Y-%m-%d"))]
    return rows


def df_to_feature(data: pd.DataFrame) -> list[geojson.Feature]:
    features = []
    for record in data.to_dict(orient='records'):
        lon = record.pop('LONGITUDE')
        lat = record.pop('LATITUDE')
        feature = geojson.Feature(geometry=geojson.Point((lon, lat)), properties=record)
        features.append(feature)
    return features


async def main(start: dt.datetime, end: dt.datetime) -> None:
    page_url = f'{BASE_URL}{end.year}/'
    feature_collection = geojson.FeatureCollection([])

    # Download base page
    async with aiohttp.ClientSession() as session:
        async with session.get(page_url) as response:
            html = await response.text(encoding='utf-8')

        # Parsing page into filtered links
        links: Iterator[str] = filter_links(parse_page_to_links(html))

        # Download datasets from every link and add it to feature collection.
        async for csv_file in bulk_download_csv(links, page_url, session):
            rows: pd.DataFrame = find_rows_by_date(csv_file, start, end)
            if not rows.empty:
                feature_collection.features.extend(df_to_feature(rows))

    # Save result
    async with aiofiles.open(BASE_DIR / 'result.geojson', "w", encoding="utf-8") as f:
        await f.write(geojson.dumps(feature_collection, indent=4))


if __name__ == "__main__":
    end_datetime = dt.datetime.now()
    start_datetime = end_datetime - dt.timedelta(days=4)
    asyncio.run(main(start_datetime, end_datetime))
