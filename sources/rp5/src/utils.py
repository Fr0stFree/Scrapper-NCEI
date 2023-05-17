import shutil
import sys
from pathlib import Path
from typing import Callable, Any

import geojson
import loguru
import pandas as pd

from . import exceptions


def save_geojson(data: geojson.GeoJSON, save_to: Path, name: str = 'result') -> None:
    with open(save_to / f'{name}.geojson', "w", encoding='utf-8') as f:
        f.write(geojson.dumps(data, indent=4))


def extract_csv(path: Path, **kwargs):
    return pd.read_csv(path, **kwargs)


def cleanup(path: Path) -> None:
    if path.is_dir():
        path.rmdir()
    else:
        path.unlink()


def task_error_handler(task: Callable) -> Any:
    logger = loguru.logger

    try:
        return task()

    except exceptions.ScenarioFailed as exc:
        logger.error(f'Failed to parse page {exc.url}.\nAn error occurred: {exc}')
        sys.exit(1)

    except exceptions.ConvertingFailed as exc:
        logger.error(f'Failed to convert dataframe.\nAn error occurred: {exc}')
        sys.exit(1)

    except Exception as exc:
        logger.error(f'Unhandled exception: {exc}')
        sys.exit(1)
