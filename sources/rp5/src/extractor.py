from pathlib import Path
from typing import Final, Literal

import pandas as pd

from .exceptions import InvalidStationCSV


class StationCSVExtractor:
    HEADER_ROW: Final[int] = 6
    COMPRESSION: Final[Literal['gzip']] = 'gzip'
    DELIMITER: Final[str] = ';'
    EXPECTED_HEADER: Final[list[str]] = ['T', 'Po', 'P', 'Pa', 'U', 'DD']
    DATETIME_COLUMN: Final[int] = 0
    DATETIME_FORMAT: Final[str] = '%d.%m.%Y %H:%M'

    def extract(self, path: Path) -> pd.DataFrame:
        df = pd.read_csv(
            path,
            compression=self.COMPRESSION,
            delimiter=self.DELIMITER,
            header=self.HEADER_ROW,
            index_col=False,
        )
        is_valid, reason = self._is_valid(df)
        if not is_valid:
            raise InvalidStationCSV(reason, path)
        return df

    def _is_valid(self, df: pd.DataFrame) -> tuple[bool, str]:
        if (header := df.columns.tolist()[1:1 + len(self.EXPECTED_HEADER)]) != self.EXPECTED_HEADER:
            return False, f'Invalid station csv file. Expected header: {self.EXPECTED_HEADER}. Got: {header}.'

        datetime_cell = df.iloc[0, self.DATETIME_COLUMN]
        try:
            pd.to_datetime(datetime_cell, format=self.DATETIME_FORMAT)
        except ValueError:
            return False, f'Invalid datetime format. Expected format: {self.DATETIME_FORMAT}. Got: {datetime_cell}.'

        return True, ''

    @property
    def datetime_column(self) -> int:
        return self.DATETIME_COLUMN

    @property
    def datetime_format(self) -> str:
        return self.DATETIME_FORMAT
