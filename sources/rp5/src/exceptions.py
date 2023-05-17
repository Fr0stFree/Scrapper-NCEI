from pathlib import Path


class ScenarioFailed(Exception):
    def __init__(self, message: str, url: str) -> None:
        super(ScenarioFailed, self).__init__(message)
        self.message = message
        self.url = url


class InvalidStationCSV(Exception):
    def __init__(self, message: str, path: Path) -> None:
        super(InvalidStationCSV, self).__init__(message)
        self.path = path


class ConvertingFailed(Exception):
    def __init__(self, message: str) -> None:
        super(ConvertingFailed, self).__init__(message)
        self.message = message
