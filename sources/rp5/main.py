import datetime as dt

from src import stations, settings, FeatureProcessor
from src.utils import save_geojson, cleanup
from src.webdriver import ChromeDriver, RP5ParseScenario

if __name__ == '__main__':
    max_date = dt.datetime.now().date()
    min_date = max_date - dt.timedelta(settings.DATA_AMOUNT_IN_DAYS)

    processor = FeatureProcessor()
    with RP5ParseScenario(ChromeDriver, min_date, max_date) as scenario:
        for station in stations.values():
            file_path = settings.TEMP_DIR / station.id
            scenario.download(station.url, save_to=file_path)
            processor.process(file_path, coordinates=(station.longitude, station.latitude))

    save_geojson(data=processor.result, path=settings.DATA_DIR)
    cleanup(settings.TEMP_DIR)
