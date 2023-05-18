import pytest
from pathlib import Path

from src.extractor import StationCSVExtractor
from src.converter import CSVToFeatureConverter
from src import settings


@pytest.fixture(scope='function')
def extractor():
    extractor = StationCSVExtractor()
    yield extractor
    del extractor


@pytest.fixture(scope='function')
def converter(extractor):
    converter = CSVToFeatureConverter(datetime_column=extractor.datetime_column,
                                      datetime_format=extractor.datetime_format)
    yield converter
    del converter
