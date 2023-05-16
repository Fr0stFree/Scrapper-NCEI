from pathlib import Path
from typing import Literal, Final

import geojson
import numpy as np
import pandas as pd


class FeatureProcessor:
    HEADER_COLUMN: Final[int] = 6
    DELIMITER: Final[str] = ';'
    COMPRESSION: Literal['gzip'] = 'gzip'
    INDEX_COLUMN: Final[bool] = False
    DATETIME_FORMAT: Final[str] = '%d.%m.%Y %H:%M'

    def __init__(self) -> None:
        self._result = geojson.FeatureCollection([])

    def process(self, path: Path, coordinates: tuple[float, float]) -> None:
        df = pd.read_csv(
            path,
            compression=self.COMPRESSION,
            delimiter=self.DELIMITER,
            header=self.HEADER_COLUMN,
            index_col=self.INDEX_COLUMN,
        )
        df.replace(np.nan, None, inplace=True)
        df.rename(columns={df.columns[0]: 'DATETIME'}, inplace=True)
        features = self._csv_to_features(data=df, coordinates=coordinates)
        self._result.features.extend(features)

    def _csv_to_features(self, data: pd.DataFrame, coordinates: tuple[float, float]) -> list[geojson.Feature]:
        features = []

        for record in data.to_dict(orient='records'):
            feature = geojson.Feature(geometry=geojson.Point(coordinates), properties=record)
            features.append(feature)

        return features

    @property
    def result(self) -> geojson.FeatureCollection:
        return self._result
