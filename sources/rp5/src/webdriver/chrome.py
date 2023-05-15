import datetime as dt
from pathlib import Path
from typing import Self

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .locators import Locator, ArchivePage
from .interface import DriverInterface


class ChromeDriver(DriverInterface):
    FAKE_USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0"

    def __init__(self, storage_path: Path, wait_limit: int = 5) -> None:
        self._wait_limit = wait_limit
        self._options = self._set_options(storage_path)

    def _set_options(self, storage_folder: Path | None) -> Options:
        options = Options()
        options.add_argument(f'User-Agent={self.FAKE_USER_AGENT}')
        if storage_folder is not None:
            options.add_argument(f'download.default_directory={storage_folder}')
        return options

    def __enter__(self) -> Self:
        self._chrome = webdriver.Chrome(chrome_options=self._options)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._chrome.close()

    def open(self, url: str) -> None:
        return self._chrome.get(url)

    def goto_archive_tab(self) -> None:
        self._press_on(ArchivePage.ARCHIVE_DOWNLOAD_TAB)

    def select_csv_format(self) -> None:
        self._press_on(ArchivePage.CSV_FORMAT_RADIO_BUTTON)

    def select_utf8_encoding(self) -> None:
        self._press_on(ArchivePage.UTF8_ENCODING_RADIO_BUTTON)

    def enter_min_calendar_date(self, date: dt.date) -> None:
        self._enter_in(ArchivePage.START_DATE_INPUT, date.strftime('%d.%m.%Y'))

    def enter_max_calendar_date(self, date: dt.date) -> None:
        self._enter_in(ArchivePage.END_DATE_INPUT, date.strftime('%d.%m.%Y'))

    def request_archive(self) -> None:
        self._press_on(ArchivePage.REQUEST_ARCHIVE_BUTTON)

    def download_archive(self) -> None:
        self._press_on(ArchivePage.DOWNLOAD_ARCHIVE_BUTTON)

    def _enter_in(self, locator: Locator, value: str) -> None:
        element = self._chrome.find_element(*locator)
        element.clear()
        element.send_keys(value)

    def _press_on(self, locator: Locator) -> None:
        WebDriverWait(self._chrome, self._wait_limit).until(EC.element_to_be_clickable(locator))
        self._chrome.find_element(*locator).click()
