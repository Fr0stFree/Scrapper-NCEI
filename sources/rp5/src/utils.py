import shutil
from pathlib import Path

import geojson
import pandas as pd


def save_geojson(data: geojson.GeoJSON, path: Path, name: str = 'result') -> None:
    with open(path / f'{name}.geojson', "w", encoding='utf-8') as f:
        f.write(geojson.dumps(data, indent=4))


def extract_csv(path: Path, **kwargs):
    return pd.read_csv(path, **kwargs)



def cleanup(path: Path) -> None:
    shutil.rmtree(path)
