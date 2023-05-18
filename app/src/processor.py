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

    def __init__(self) -> None:
        self._result = geojson.FeatureCollection([])

    def process(self, csv_file: str, start_date: dt.date, end_date: dt.date) -> None:
        df = self._find_rows_by_date(csv_file, start_date, end_date)
        if not df.empty:
            features = self._convert_df_to_feature_list(df)
            self._result.features.extend(features)

    def _find_rows_by_date(self, csv_file: str, start_date: dt.date, end_date: dt.date) -> pd.DataFrame:
        df = pd.read_csv(io.StringIO(csv_file), sep=self.CSV_SEPARATOR, header=0)
        rows = df.loc[(df[self.DATE_COLUMN_NAME] >= start_date.strftime(self.DATE_FORMAT)) &
                      (df[self.DATE_COLUMN_NAME] <= end_date.strftime(self.DATE_FORMAT))]
        return rows

    def _convert_df_to_feature_list(self, data: pd.DataFrame) -> list[geojson.Feature]:
        features = []
        for record in data.to_dict(orient='records'):
            lon = record.pop(self.LONGITUDE_COLUMN_NAME)
            lat = record.pop(self.LATITUDE_COLUMN_NAME)
            feature = geojson.Feature(geometry=geojson.Point((lon, lat)), properties=record)
            features.append(feature)
        return features

    @property
    def result(self) -> geojson.FeatureCollection:
        return self._result

