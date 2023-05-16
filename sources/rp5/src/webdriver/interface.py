import datetime as dt
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Self

from .locators import Locator


class DriverInterface(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def start(self) -> Self:
        pass

    @abstractmethod
    def finish(self) -> None:
        pass

    @abstractmethod
    def open(self, url: str) -> None:
        pass

    @abstractmethod
    def goto_archive_tab(self, locator: Locator) -> None:
        pass

    @abstractmethod
    def select_csv_format(self, locator: Locator) -> None:
        pass

    @abstractmethod
    def select_utf8_encoding(self, locator: Locator) -> None:
        pass

    @abstractmethod
    def enter_min_calendar_date(self, locator: Locator, date: dt.date) -> None:
        pass

    @abstractmethod
    def enter_max_calendar_date(self, locator: Locator, date: dt.date) -> None:
        pass

    @abstractmethod
    def request_archive(self, locator: Locator) -> None:
        pass

    @abstractmethod
    def download_archive(self, locator: Locator, save_to: Path) -> None:
        pass

