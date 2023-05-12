import time
from pathlib import Path

from selenium.webdriver.common.by import By

from .stations import stations
from .webdriver import ChromeDriver

TEMP_DIR: Path = Path(__file__).parent / 'temp'

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
    with ChromeDriver() as browser:
        for station in stations:
            browser.get(station.url)

            # change page to archives
            browser.find_element(By.ID, 'tabSynopDLoad').click()

            # set format to scv
            browser.find_element(By.XPATH, '//label[contains(text(), "CSV")]/span').click()

            # set encoding to utf-8
            browser.find_element(By.XPATH, '//label[contains(text(), "UTF-8")]/span').click()

            time.sleep(5)
