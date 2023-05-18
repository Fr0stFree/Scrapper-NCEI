import datetime as dt

import geojson

from src import Station, stations, settings
from src.converter import CSVToFeatureConverter
from src.webdriver import ChromeDriver
from src.scenario import RP5ParseScenario
from src.extractor import StationCSVExtractor
from src.utils import save_geojson, cleanup, task_error_handler


@task_error_handler
def get_station_feature_collection(station: Station,
                                   extractor: StationCSVExtractor,
                                   scenario: RP5ParseScenario,
                                   converter: CSVToFeatureConverter) -> geojson.FeatureCollection:
    file_path = settings.TEMP_DIR / station.id

    scenario.download(url=station.url, save_to=file_path)
    df = extractor.extract(file_path)
    extra_props = {'id': station.id, 'name': station.name}
    feature_collection = converter.df_to_collection(df, coordinates=(station.longitude, station.latitude),
                                                    **extra_props)

    cleanup(file_path)
    return feature_collection


if __name__ == '__main__':
    max_date = dt.datetime.now().date()
    min_date = max_date - dt.timedelta(settings.DATA_AMOUNT_IN_DAYS)
    data = geojson.FeatureCollection([])

    with RP5ParseScenario(ChromeDriver, min_date, max_date) as scenario:
        extractor = StationCSVExtractor()
        converter = CSVToFeatureConverter(datetime_column=extractor.datetime_column,
                                          datetime_format=extractor.datetime_format)
        for station in stations:
            collection = get_station_feature_collection(station, extractor, scenario, converter)
            data.update(collection)

    save_geojson(data, save_to=settings.DATA_DIR)
    cleanup(settings.TEMP_DIR)
