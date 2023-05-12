from pathlib import Path
from typing import Iterable

import geojson


class Manipulator:
    @staticmethod
    def load_stations(path: Path) -> Iterable[str]:
        with open(path) as f:
            return set([station_id for station_id in f.read().split()])

    @staticmethod
    def save_geojson(data: geojson.GeoJSON, path: Path, name: str = 'result') -> None:
        with open(path / f'{name}.geojson', "w", encoding="utf-8") as f:
            f.write(geojson.dumps(data, indent=4))
