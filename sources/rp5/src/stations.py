from typing import NamedTuple


class Station(NamedTuple):
    id: str
    name: str
    latitude: float
    longitude: float
    url: str


stations: list[Station] = [
    Station('22113', 'Murmanks', 68.915173, 33.098581, 'https://rp5.ru/Архив_погоды_в_Мурманске'),
    Station('22292', 'Indiga', 67.686944, 49.016667, 'https://rp5.ru/Архив_погоды_в_Индиге'),
    Station('22165', 'Cape Kanin Nos ', 68.657222, 43.273889, 'https://rp5.ru/Архив_погоды_на_мысе_Канин_Нос'),
    Station('23103', 'Khodovarikha', 68.933089, 53.758690, 'https://rp5.ru/Архив_погоды_в_Ходоварихе'),
    Station('23112', 'Varandey', 68.824039, 58.068760, 'https://rp5.ru/Архив_погоды_в_Варандее'),
    Station('20946', 'Cape Bolvansky', 70.447222, 59.088333, 'https://rp5.ru/Архив_погоды_на_мысе_Болванский'),
    Station('23022', 'Amderma', 69.764400, 61.685300, 'https://rp5.ru/Архив_погоды_в_Амдерме'),
    Station('23032', 'Marrasale', 69.716667, 66.800000, 'https://rp5.ru/Архив_погоды_в_Марресале'),
    Station('23029', 'Ust\'-Kara', 69.250000, 64.966667, 'https://rp5.ru/Архив_погоды_в_Усть-Каре'),
    Station('20667', 'Station named after M.V.Popov', 73.333333, 70.050000,
            'https://rp5.ru/Архив_погоды_на_метеостанции_им._М.В.Попова'),
]
