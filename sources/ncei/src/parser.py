from typing import Iterator, Generator, Final, Iterable

from bs4 import BeautifulSoup


class PageParser:
    HTML_PARSER: Final[str] = "lxml"

    @classmethod
    def parse(cls, station_ids: Iterable[str], page: str) -> Iterator[str]:
        links = cls._parse_page_to_links(page)
        return cls._filter_links(links, station_ids)

    @classmethod
    def _parse_page_to_links(cls, page: str) -> Generator[str, None, None]:
        soup = BeautifulSoup(page, cls.HTML_PARSER)
        table = soup.find("table")
        return (link["href"] for link in table.find_all("a"))

    @classmethod
    def _filter_links(cls, links: Generator[str, None, None], station_ids: Iterable[str]) -> Iterator[str]:
        return filter(lambda link: any([link.startswith(station_id) for station_id in station_ids]), links)
