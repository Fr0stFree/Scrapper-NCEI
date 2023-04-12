import asyncio
import datetime as dt
import io
from array import array
from pathlib import Path
from typing import Iterator, AsyncGenerator

import aiofiles
import aiohttp
import geojson
import pandas as pd
from bs4 import BeautifulSoup

BASE_DIR: Path = Path(__file__).parent
STORAGE_DIR: Path = BASE_DIR / 'storage'
SEMAPHORE_LIMIT: int = 5


with open(BASE_DIR / 'stations.txt') as f:
    STATIONS_IDS = [station_id for station_id in f.read().split()]


def parse_page_to_links(html: str) -> Iterator[str]:
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    return (link["href"] for link in table.find_all("a"))


def filter_links(links: Iterator[str]) -> Iterator[str]:
    return filter(lambda link: any([link.startswith(station_id) for station_id in STATIONS_IDS]), links)


async def download_csv(link: str, session: aiohttp.ClientSession, semaphore: asyncio.Semaphore):
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
            csv_file = await task
        except Exception as e:
            print('Невозможно скачать файл. Произошла ошибка:', e)
            continue
        else:
            yield csv_file


def find_row_by_date(csv_file: str, date: dt.datetime) -> pd.DataFrame:
    df = pd.read_csv(io.StringIO(csv_file), sep=',', header=0)
    row = df.loc[df['DATE'] == date.strftime("%Y-%m-%d")]
    return row


def df_to_feature(data: pd.DataFrame) -> geojson.Feature:
    dict_data = data.to_dict(orient='records')[0]
    lon = dict_data.pop('LONGITUDE')
    lat = dict_data.pop('LATITUDE')
    return geojson.Feature(geometry=geojson.Point((lon, lat)), properties=dict_data)
    

async def main(looking_date: dt.datetime):
    page_url: str = f'https://www.ncei.noaa.gov/data/global-summary-of-the-day/access/{looking_date.year}/'
    feature_collection = geojson.FeatureCollection([])

    async with aiohttp.ClientSession() as session:
        async with session.get(page_url) as response:
            html = await response.text()

        links = parse_page_to_links(html)
        looking_links = filter_links(links)

        async for csv_file in bulk_download_csv(looking_links, page_url, session):
            row: pd.DataFrame = find_row_by_date(csv_file, looking_date)
            if not row.empty:
                feature_collection.features.append(df_to_feature(row))

    async with aiofiles.open(STORAGE_DIR / 'result.geojson', "w", encoding="utf-8") as f:
        await f.write(geojson.dumps(feature_collection, indent=4))
    
        
if __name__ == "__main__":
    asyncio.run(main(looking_date=dt.datetime(2023, 1, 1)))
