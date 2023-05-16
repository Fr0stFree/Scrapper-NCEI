import datetime as dt

from src import stations, settings
from src.processor import FeatureProcessor
from src.utils import save_geojson, cleanup, extract_csv
from src.webdriver import ChromeDriver, RP5ParseScenario

if __name__ == '__main__':
    max_date = dt.datetime.now().date()
    min_date = max_date - dt.timedelta(settings.DATA_AMOUNT_IN_DAYS)
    processor = FeatureProcessor()

    with RP5ParseScenario(ChromeDriver, min_date, max_date) as scenario:
        for station in stations:
            file_path = settings.TEMP_DIR / station.id
            scenario.download(station.url, save_to=file_path)
            dataframe = extract_csv(file_path, compression='gzip', delimiter=';', header=6, index_col=False)
            processor.convert_df_to_geojson(dataframe, coordinates=(station.longitude, station.latitude))

    save_geojson(data=processor.result, path=settings.DATA_DIR)
    cleanup(settings.TEMP_DIR)
