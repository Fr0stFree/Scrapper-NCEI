import datetime as dt

from src import StationManager, settings, FeatureProcessor
from src.utils import save_geojson
from src.webdriver import ChromeDriver, DownloadArchivesScenario

if __name__ == '__main__':
    max_date = dt.datetime.now().date()
    min_date = max_date - dt.timedelta(settings.DATA_AMOUNT_IN_DAYS)
    stations = StationManager.all()

    scenario = DownloadArchivesScenario(ChromeDriver, stations, min_date, max_date, storage_path=settings.TEMP_DIR)
    archive_paths = scenario.run()

    processor = FeatureProcessor()
    for path in archive_paths:
        station = StationManager.get(id=path.name)
        processor.process(station, path)

    save_geojson(data=processor.result, path=settings.DATA_DIR)
