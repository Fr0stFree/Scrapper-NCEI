from pathlib import Path

import geojson


def load_stations(path: Path) -> set[str]:
    with open(path) as f:
        return set([station_id for station_id in f.read().split()])


def save_geojson(data: geojson.GeoJSON, path: Path, name: str = 'result') -> None:
    with open(path / f'{name}.geojson', "w", encoding='utf-8') as f:
        f.write(geojson.dumps(data, indent=4))
