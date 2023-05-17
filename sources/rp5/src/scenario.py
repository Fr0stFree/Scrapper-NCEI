import datetime as dt
from pathlib import Path
from typing import Type, Self

from .webdriver.interface import DriverInterface
from .webdriver.locators import ArchivePage
from .exceptions import ScenarioFailed


class RP5ParseScenario:
    def __init__(self, driver: Type[DriverInterface],
                 min_date: dt.date,
                 max_date: dt.date) -> None:
        self._Driver = driver
        self._min_date = min_date
        self._max_date = max_date
        self._driver_instance: DriverInterface | None = None

    def __enter__(self, *args, **kwargs) -> Self:
        self._driver_instance = self._Driver(*args, **kwargs)
        self._driver_instance.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._driver_instance.finish()

    def download(self, url: str, save_to: Path) -> None:
        try:
            self._driver_instance.open(url)
            self._driver_instance.goto_archive_tab(ArchivePage.ARCHIVE_DOWNLOAD_TAB)
            self._driver_instance.select_csv_format(ArchivePage.CSV_FORMAT_RADIO_BUTTON)
            self._driver_instance.select_utf8_encoding(ArchivePage.UTF8_ENCODING_RADIO_BUTTON)
            self._driver_instance.enter_min_calendar_date(ArchivePage.START_DATE_INPUT, date=self._min_date)
            self._driver_instance.enter_max_calendar_date(ArchivePage.END_DATE_INPUT, date=self._max_date)
            self._driver_instance.request_archive(ArchivePage.REQUEST_ARCHIVE_BUTTON)
            self._driver_instance.download_archive(ArchivePage.DOWNLOAD_ARCHIVE_BUTTON, save_to)
        except Exception as exc:
            raise ScenarioFailed(f'Unable to parse page: {url}. An error occurred: {exc}')

