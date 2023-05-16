import geojson
import numpy as np
import pandas as pd


class FeatureProcessor:
    def __init__(self) -> None:
        self._result = geojson.FeatureCollection([])

    __slots__ = ('_result', )

    def convert_df_to_geojson(self, df: pd.DataFrame, coordinates: tuple[float, float]) -> None:
        df = self._prepare_df(df)
        features = self._convert_df_to_features(data=df, coordinates=coordinates)
        self._result.features.extend(features)

    @staticmethod
    def _prepare_df(df: pd.DataFrame) -> pd.DataFrame:
        df.replace(np.nan, None, inplace=True)
        df.rename(columns={df.columns[0]: 'DATETIME'}, inplace=True)
        return df

    @staticmethod
    def _convert_df_to_features(data: pd.DataFrame, coordinates: tuple[float, float]) -> list[geojson.Feature]:
        features = []
        for record in data.to_dict(orient='records'):
            feature = geojson.Feature(geometry=geojson.Point(coordinates), properties=record)
            features.append(feature)
        return features

    @property
    def result(self) -> geojson.FeatureCollection:
        return self._result
