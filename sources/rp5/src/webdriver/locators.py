from typing import NamedTuple

from selenium.webdriver.common.by import By


class Locator(NamedTuple):
    by: str
    value: str


class ArchivePage:
    ARCHIVE_DOWNLOAD_TAB = Locator(By.ID, 'tabSynopDLoad')
    CSV_FORMAT_RADIO_BUTTON = Locator(By.XPATH, '//label[input/@id="format2"]/span')
    UTF8_ENCODING_RADIO_BUTTON = Locator(By.XPATH, '//label[input/@id="coding2"]/span')
    START_DATE_INPUT = Locator(By.ID, 'calender_dload')
    END_DATE_INPUT = Locator(By.ID, 'calender_dload2')
    REQUEST_ARCHIVE_BUTTON = Locator(By.CSS_SELECTOR, 'td.download > div.archButton')
    DOWNLOAD_ARCHIVE_BUTTON = Locator(By.CSS_SELECTOR, 'span#f_result > a')
