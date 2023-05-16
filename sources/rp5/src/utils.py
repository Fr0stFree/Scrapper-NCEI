import shutil
from pathlib import Path

import geojson


def save_geojson(data: geojson.GeoJSON, path: Path, name: str = 'result') -> None:
    with open(path / f'{name}.geojson', "w", encoding='utf-8') as f:
        f.write(geojson.dumps(data, indent=4))


def cleanup(path: Path) -> None:
    shutil.rmtree(path)
