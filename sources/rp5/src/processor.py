from pathlib import Path
from typing import Iterable, Literal

import geojson
import pandas as pd


class DataProcessor:
    def __init__(self, compression: Literal['gzip'], delimiter: str, header_column: int) -> None:
        self._compression = compression
        self._delimiter = delimiter
        self._header_column = header_column
        self._result = geojson.FeatureCollection([])

    def process(self, paths: Iterable[Path]) -> geojson.FeatureCollection:
        for path in paths:
            df = pd.read_csv(path, compression=self._compression, delimiter=self._delimiter, header=self._header_column)
            self.add_features(data=df, coordinates=(50.5, 50.5))
            break
        return self._result

    def add_features(self, data: pd.DataFrame, coordinates: tuple[float, float] = (50.5, 50.5)) -> None:
        # for record in data.to_json():

        feature = geojson.Feature(geometry=geojson.Point(coordinates), properties=...)
        self._result.features.append(feature)

