from pathlib import Path

import pytest
import loguru

from src import settings, exceptions
from src.utils import cleanup, save_geojson

logger = loguru.logger


class TestCleanup:
    def test_cleanup_with_dir(self):
        temp_dir = settings.TEST_DIR / 'temp'
        temp_dir.mkdir()
        assert temp_dir.exists()

        cleanup(temp_dir)

        assert not temp_dir.exists()

    def test_cleanup_with_file(self):
        temp_file = settings.TEST_DIR / 'temp.txt'
        temp_file.touch()
        assert temp_file.exists()

        cleanup(temp_file)

        assert not temp_file.exists()

    def test_cleanup_with_nonexistent_dir(self):
        temp_dir = settings.TEST_DIR / 'temp'
        assert not temp_dir.exists()

        cleanup(temp_dir)

        assert not temp_dir.exists()

    def test_cleanup_with_nonexistent_file(self):
        temp_dir = settings.TEST_DIR / 'temp.txt'
        assert not temp_dir.exists()

        cleanup(temp_dir)

        assert not temp_dir.exists()

