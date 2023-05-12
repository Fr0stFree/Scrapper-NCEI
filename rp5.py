import time
from contextlib import contextmanager
from pathlib import Path
from typing import NamedTuple

from selenium import webdriver
from selenium.webdriver.common.by import By

TEMP_DIR: Path = Path(__file__).parent / 'temp'

class Station(NamedTuple):
    id: str
    name: str
    latitude: float
    longitude: float
    url: str

# STATIONS: Final[dict[str, str]] = {
#     '22113': 'Murmansk',
#     '22292': 'Indiga',
#     '22165': 'Kanin Nose',
#     '23103': 'Khodovarikha',
#     '23112': 'Varandey',
#     '20946': 'Cape Bolvansky',
#     '23022': 'Amderma',
#     '23032': 'Morrasale',
#     '20667': 'Station named after M.V.Popov',
#     '23029': 'Ust\'-Kara'
# }

STATIONS2: list[Station] = [
    Station('22113', 'Murmanks', 68.915173, 33.098581, 'https://rp5.ru/Архив_погоды_в_Мурманске'),
]


@contextmanager
def browser():
    chrome = webdriver.Chrome()
    try:
        yield chrome
    finally:
        chrome.quit()


class Driver:
    def __enter__(self) -> webdriver.Chrome:
        self.browser = webdriver.Chrome()
        return self.browser

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.browser.close()

    def run(self) -> None:
        for station in STATIONS2:
            self.browser.get(station.url)
            time.sleep(5)


    # @staticmethod
    # def _unpack_archive(path: Path) -> None:
    #     with gzip.open(path, 'rb') as data:
    #         data: IO[bytes]
    #         with io.TextIOWrapper(data, encoding='utf-8') as result:
    #             df = pd.read_fwf(result, header=5, delimiter=';')
    #
    #     path = path.with_suffix('')
    #     df.to_csv(path, index=False)


if __name__ == '__main__':
    with Driver() as browser:
        for station in STATIONS2:
            browser.get(station.url)
            go_to_achive_button = browser.find_element(By.ID, 'tabSynopDLoad')
            go_to_achive_button.click()
            time.sleep(1)
            csv_radio_button = browser.find_element(By.XPATH, '//label[contains(text(), "CSV")]/span')
            csv_radio_button.click()

            time.sleep(1)
            csv_radio_button = browser.find_element(By.XPATH, '//label[contains(text(), "UTF-8")]/span')
            csv_radio_button.click()

            time.sleep(105)
