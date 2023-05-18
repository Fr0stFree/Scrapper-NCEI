import pytest
import loguru

from src import settings
from src.exceptions import InvalidStationCSV


class TestExtractStationCsv:
    TEST_DATA_PATH = settings.TEST_DIR / 'dummy_data' / 'test_station_data.csv.gz'

    def test_extract_csv(self, extractor,):
        df = extractor.extract(self.TEST_DATA_PATH)

        assert df.shape == (13, 29)
        assert df.columns.tolist()[:4] == ['Местное время в Индиге', 'T', 'Po', 'P']
        assert df.values.tolist()[0][:4] == ['17.05.2023 15:00', 14.1, 761.7, 762.1]

    def test_extract_nonexistent_csv(self, extractor):
        with pytest.raises(FileNotFoundError):
            extractor.extract(self.TEST_DATA_PATH.parent / 'nonexistent.csv.gz')

    def test_extract_invalid_structure_csv(self, extractor, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(extractor, 'EXPECTED_HEADER', ['A', 'B', 'C', 'D', 'E', 'F'])

            with pytest.raises(InvalidStationCSV) as excinfo:
                extractor.extract(self.TEST_DATA_PATH)

    def test_extract_invalid_datetime_csv(self, extractor, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(extractor, 'DATETIME_FORMAT', '%d/%m/%Y %H:%M')

            with pytest.raises(InvalidStationCSV) as excinfo:
                extractor.extract(self.TEST_DATA_PATH)
