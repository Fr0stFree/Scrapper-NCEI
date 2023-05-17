import pytest
import loguru

from src import settings
from src.extractor import StationCSVExtractor
from src.exceptions import InvalidStationCSV


logger = loguru.logger


class TestExtractStationCsv:
    def test_extract_csv(self):
        path = settings.TEST_DIR / 'dummy_data' / 'test_station_data.csv.gz'
        extractor = StationCSVExtractor()

        df = extractor.extract(path)

        assert df.shape == (13, 29)
        assert df.columns.tolist()[:4] == ['Местное время в Индиге', 'T', 'Po', 'P']
        assert df.values.tolist()[0][:4] == ['17.05.2023 15:00', 14.1, 761.7, 762.1]

    def test_extract_nonexistent_csv(self):
        path = settings.TEST_DIR / 'dummy_data' / 'nonexistent.csv.gz'
        extractor = StationCSVExtractor()

        with pytest.raises(FileNotFoundError):
            extractor.extract(path)

    def test_extract_invalid_structure_csv(self, monkeypatch):
        path = settings.TEST_DIR / 'dummy_data' / 'test_station_data.csv.gz'
        extractor = StationCSVExtractor()

        with monkeypatch.context() as m:
            m.setattr(extractor, 'EXPECTED_HEADER', ['A', 'B', 'C', 'D', 'E', 'F'])

            with pytest.raises(InvalidStationCSV) as excinfo:
                extractor.extract(path)

    def test_extract_invalid_datetime_csv(self, monkeypatch):
        path = settings.TEST_DIR / 'dummy_data' / 'test_station_data.csv.gz'
        extractor = StationCSVExtractor()

        with monkeypatch.context() as m:
            m.setattr(extractor, 'DATETIME_FORMAT', '%d/%m/%Y %H:%M')

            with pytest.raises(InvalidStationCSV) as excinfo:
                extractor.extract(path)