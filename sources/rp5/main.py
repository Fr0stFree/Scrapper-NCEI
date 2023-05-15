import datetime as dt

import pandas as pd


from src import stations, settings, DataProcessor
from src.utils import save_geojson
# from src.webdriver import ChromeDriver


if __name__ == '__main__':
    max_date = dt.datetime.now().date()
    min_date = max_date - dt.timedelta(settings.DATA_AMOUNT_IN_DAYS)
    urls = (station.url for station in stations)

    # TODO: протестировать работоспособность сохранения в TEMP_DIR
    # archive_paths = ChromeDriver.download_archives(urls, min_date, max_date, storage_path=settings.TEMP_DIR)

    archive_paths = (file for file in settings.TEMP_DIR.iterdir() if file.suffix == '.gz')
    # file_paths = unpack_archives(archive_paths)

    processor = DataProcessor(compression='gzip', delimiter=';', header_column=6)
    feature_collection = processor.process(archive_paths)

    save_geojson(feature_collection, path=settings.DATA_DIR)
