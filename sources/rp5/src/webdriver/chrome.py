import datetime as dt
from pathlib import Path
from typing import Self

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .interface import DriverInterface
from .locators import Locator


class ChromeDriver(DriverInterface):
    FAKE_USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0"
    WAIT_LIMIT: int = 5  # sec

    def __init__(self) -> None:
        self._options = Options()
        self._options.add_argument(f'User-Agent={self.FAKE_USER_AGENT}')

    def start(self) -> Self:
        self._session = requests.session()
        self._session.headers = {'User-Agent': self.FAKE_USER_AGENT}
        self._chrome = webdriver.Chrome(options=self._options)
        return self

    def finish(self) -> None:
        self._session.close()
        self._chrome.close()

    def open(self, url: str) -> None:
        return self._chrome.get(url)

    def goto_archive_tab(self, element_locator: Locator) -> None:
        self._press_on(element_locator)

    def select_csv_format(self, element_locator: Locator) -> None:
        self._press_on(element_locator)

    def select_utf8_encoding(self, element_locator: Locator) -> None:
        self._press_on(element_locator)

    def enter_min_calendar_date(self, element_locator: Locator, date: dt.date) -> None:
        self._enter_in(element_locator, date.strftime('%d.%m.%Y'))

    def enter_max_calendar_date(self, element_locator: Locator, date: dt.date) -> None:
        self._enter_in(element_locator, date.strftime('%d.%m.%Y'))

    def request_archive(self, element_locator: Locator) -> None:
        self._press_on(element_locator)

    def download_archive(self, element_locator: Locator, save_to: Path) -> None:
        self._wait_for_element(element_locator)
        url = self._chrome.find_element(*element_locator).get_attribute('href')
        response = self._session.get(url)
        with open(save_to, 'wb') as file:
            file.write(response.content)

    def _enter_in(self, element_locator: Locator, value: str) -> None:
        self._wait_for_element(element_locator)
        element = self._chrome.find_element(*element_locator)
        element.clear()
        element.send_keys(value)

    def _press_on(self, element_locator: Locator) -> None:
        self._wait_for_element(element_locator)
        self._chrome.find_element(*element_locator).click()

    def _wait_for_element(self, element_locator: Locator) -> None:
        WebDriverWait(self._chrome, self.WAIT_LIMIT).until(EC.element_to_be_clickable(element_locator))
