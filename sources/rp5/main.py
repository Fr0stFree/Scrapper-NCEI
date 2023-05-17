import datetime as dt

import geojson

from src import Station, stations, settings
from src.converter import CSVToFeatureConverter
from src.utils import save_geojson, cleanup, extract_csv, task_error_handler
from src.webdriver import ChromeDriver
from src.scenario import RP5ParseScenario


@task_error_handler
def get_station_feature_collection(station: Station, converter: CSVToFeatureConverter) -> geojson.FeatureCollection:
    file_path = settings.TEMP_DIR / station.id
    scenario.download(station.url, save_to=file_path)
    dataframe = extract_csv(file_path, compression='gzip', delimiter=';', header=6, index_col=False)
    extra_props = {'id': station.id, 'name': station.name}
    collection = converter.df_to_collection(dataframe,
                                            coordinates=(station.longitude, station.latitude),
                                            **extra_props)
    cleanup(file_path)
    return collection


if __name__ == '__main__':
    max_date = dt.datetime.now().date()
    min_date = max_date - dt.timedelta(settings.DATA_AMOUNT_IN_DAYS)
    data = geojson.FeatureCollection([])

    converter = CSVToFeatureConverter(dt_column=0, dt_format='%d.%m.%Y %H:%M')
    with RP5ParseScenario(ChromeDriver, min_date, max_date) as scenario:
        for station in stations:
            collection = get_station_feature_collection(station, converter)

    save_geojson(data, save_to=settings.DATA_DIR)
    cleanup(settings.TEMP_DIR)
