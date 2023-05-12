from selenium import webdriver


class ChromeDriver:
    def __enter__(self) -> webdriver.Chrome:
        self.browser = webdriver.Chrome()
        return self.browser

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.browser.close()
