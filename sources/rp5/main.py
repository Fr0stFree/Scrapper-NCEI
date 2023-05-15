import datetime as dt

from src import stations, settings
from src.utils import download_archives

if __name__ == '__main__':
    max_date = dt.datetime.now().date()
    min_date = max_date - dt.timedelta(settings.DATA_AMOUNT_IN_DAYS)
    urls = (station.url for station in stations)

    # TODO: протестировать работоспособность сохранения в TEMP_DIR
    download_archives(urls, min_date, max_date, storage_path=settings.TEMP_DIR)

    archive_paths = (file for file in settings.TEMP_DIR.iterdir() if file.suffix == '.gz')
    # unpack_archives(archive_paths)





