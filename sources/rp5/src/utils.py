import sys
from pathlib import Path
from typing import Callable, Any

import geojson
import loguru
import pandas as pd

from . import exceptions


logger = loguru.logger


def save_geojson(data: geojson.GeoJSON, save_to: Path, name: str = 'result') -> None:
    with open(save_to / f'{name}.geojson', "w", encoding='utf-8') as f:
        f.write(geojson.dumps(data, indent=4))


def cleanup(path: Path) -> None:
    try:
        if path.is_dir():
            path.rmdir()
        else:
            path.unlink()
    except FileNotFoundError:
        logger.warning(f'File or dir on {path} does not exist.')


def task_error_handler(task: Callable) -> Any:
    try:
        return task()

    except exceptions.ScenarioFailed as exc:
        logger.error(f'Failed to parse page {exc.url}.\n'
                     f'An error occurred: {exc}')
        sys.exit(1)

    except exceptions.ConvertingFailed as exc:
        logger.error(f'Failed to convert dataframe.\n'
                     f'An error occurred: {exc}')
        sys.exit(1)

    except exceptions.InvalidStationCSV as exc:
        logger.error(f'Failed to parse station csv file {exc.path}.\n'
                     f'An error occurred: {exc}')

    except Exception as exc:
        logger.error(f'Unhandled exception: {exc}')
        sys.exit(1)
