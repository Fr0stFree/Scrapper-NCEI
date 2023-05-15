import datetime as dt
import gzip
import io
from pathlib import Path
from typing import Iterable

import pandas as pd

from .driver import Driver


def download_archives(urls: Iterable[str], min_date: dt.date, max_date: dt.date, storage_path: Path) -> None:
    with Driver(storage_path=storage_path) as browser:
        for url in urls:
            browser.open(url)
            browser.goto_archive_tab()
            browser.select_csv_format()
            browser.select_utf8_encoding()
            browser.enter_min_calendar_date(min_date)
            browser.enter_max_calendar_date(max_date)
            browser.request_archive()
            browser.download_archive()


def unpack_archives(paths: Iterable[Path]) -> list[Path]:
    result = []

    for path in paths:
        with gzip.open(path, 'rb') as archive:
            with io.TextIOWrapper(archive, encoding='utf-8') as data:
                df = pd.read_fwf(data, header=5, delimiter=';')
        path = path.with_suffix('')
        df.to_csv(path, index=False)
        result.append(path)

    return result
