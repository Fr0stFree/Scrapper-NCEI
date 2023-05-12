import datetime as dt
import io
from typing import Final

import geojson
import pandas as pd


class DataProcessor:
    DATE_FORMAT: Final[str] = '%Y-%m-%d'
    CSV_SEPARATOR: Final[str] = ','
    DATE_COLUMN_NAME: Final[str] = 'DATE'
    LONGITUDE_COLUMN_NAME: Final[str] = 'LONGITUDE'
    LATITUDE_COLUMN_NAME: Final[str] = 'LATITUDE'

    result = geojson.FeatureCollection([])

    @classmethod
    def run(cls, csv_file: str, start_date: dt.date, end_date: dt.date) -> list[geojson.Feature] | None:
        df = cls._find_rows_by_date(csv_file, start_date, end_date)
        if not df.empty:
            features = cls._convert_df_to_feature_list(df)
            cls.result.features.extend(features)
            return features
        return None

    @classmethod
    def _find_rows_by_date(cls, csv_file: str, start_date: dt.date, end_date: dt.date) -> pd.DataFrame:
        df = pd.read_csv(io.StringIO(csv_file), sep=cls.CSV_SEPARATOR, header=0)
        rows = df.loc[(df[cls.DATE_COLUMN_NAME] >= start_date.strftime(cls.DATE_FORMAT)) &
                      (df[cls.DATE_COLUMN_NAME] <= end_date.strftime(cls.DATE_FORMAT))]
        return rows

    @classmethod
    def _convert_df_to_feature_list(cls, data: pd.DataFrame) -> list[geojson.Feature]:
        features = []
        for record in data.to_dict(orient='records'):
            lon = record.pop(cls.LONGITUDE_COLUMN_NAME)
            lat = record.pop(cls.LATITUDE_COLUMN_NAME)
            feature = geojson.Feature(geometry=geojson.Point((lon, lat)), properties=record)
            features.append(feature)
        return features

