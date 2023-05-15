import datetime as dt
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Self, Iterable, Final

from .. import settings


class DriverInterface(ABC):
    @abstractmethod
    def __init__(self, storage_path: Path, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def __enter__(self) -> Self:
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

    @abstractmethod
    def open(self, url: str) -> None:
        pass

    @abstractmethod
    def goto_archive_tab(self) -> None:
        pass

    @abstractmethod
    def select_csv_format(self) -> None:
        pass

    @abstractmethod
    def select_utf8_encoding(self) -> None:
        pass

    @abstractmethod
    def enter_min_calendar_date(self, date: dt.date) -> None:
        pass

    @abstractmethod
    def enter_max_calendar_date(self, date: dt.date) -> None:
        pass

    @abstractmethod
    def request_archive(self) -> None:
        pass

    @abstractmethod
    def download_archive(self) -> None:
        pass

    @classmethod
    def download_archives(cls, urls: Iterable[str],
                          min_date: dt.date,
                          max_date: dt.date,
                          storage_path: Path,
                          *args, **kwargs):
        with cls(storage_path, *args, **kwargs) as driver:
            for url in urls:
                driver.open(url)
                driver.goto_archive_tab()
                driver.select_csv_format()
                driver.select_utf8_encoding()
                driver.enter_min_calendar_date(min_date)
                driver.enter_max_calendar_date(max_date)
                driver.request_archive()
                driver.download_archive()

        return (file for file in storage_path.iterdir() if file.suffix == '.gz')
