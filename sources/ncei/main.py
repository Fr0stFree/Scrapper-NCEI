import asyncio
from urllib.parse import urljoin

from src import DataProcessor, PageDownloader, PageParser
from src import settings
from src.utils import load_stations, save_geojson


async def main() -> None:
    station_ids: set = load_stations(settings.BASE_DIR / 'data' / 'stations.txt')
    downloader = PageDownloader(semaphore_limit=4)
    parser = PageParser(html_parser='lxml')
    processor = DataProcessor()

    page = await downloader.get(settings.BASE_URL)
    relative_links = parser.parse(station_ids, page)
    urls = (urljoin(settings.BASE_URL, link) for link in relative_links)

    async for csv_file in downloader.get_concurrently(urls):
        processor.process(csv_file, start_date=settings.START_DATE, end_date=settings.END_DATE)

    save_geojson(data=processor.result, path=settings.BASE_DIR / 'data')


if __name__ == "__main__":
    asyncio.run(main())
