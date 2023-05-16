import datetime as dt
from pathlib import Path
from typing import Type, Iterable

from .interface import DriverInterface
from .locators import ArchivePage
from ..stations import Station


class DownloadArchivesScenario:
    def __init__(self,
                 driver: Type[DriverInterface],
                 /,
                 stations: Iterable[Station],
                 min_date: dt.date,
                 max_date: dt.date,
                 storage_path: Path) -> None:
        self._Driver = driver
        self._stations = stations
        self._min_date = min_date
        self._max_date = max_date
        self._storage_path = storage_path

    def run(self, *args, **kwargs) -> list[Path]:
        archive_paths = []

        with self._Driver(*args, storage_folder=self._storage_path, **kwargs) as driver:
            for station in self._stations:
                driver.open(station.url)
                driver.goto_archive_tab(ArchivePage.ARCHIVE_DOWNLOAD_TAB)
                driver.select_csv_format(ArchivePage.CSV_FORMAT_RADIO_BUTTON)
                driver.select_utf8_encoding(ArchivePage.UTF8_ENCODING_RADIO_BUTTON)
                driver.enter_min_calendar_date(ArchivePage.START_DATE_INPUT, date=self._min_date)
                driver.enter_max_calendar_date(ArchivePage.END_DATE_INPUT, date=self._max_date)
                driver.request_archive(ArchivePage.REQUEST_ARCHIVE_BUTTON)
                file_path = driver.download_archive(ArchivePage.DOWNLOAD_ARCHIVE_BUTTON, file_name=station.id)
                archive_paths.append(file_path)

        return archive_paths


