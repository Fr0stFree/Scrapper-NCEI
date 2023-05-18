from typing import Iterator, Generator, Iterable

from bs4 import BeautifulSoup


class PageParser:
    def __init__(self, html_parser: str = 'lxml') -> None:
        self._html_parser = html_parser

    def parse(self, station_ids: Iterable[str], page: str) -> Iterator[str]:
        links = self._parse_page_to_links(page)
        return self._filter_links(links, station_ids)

    def _parse_page_to_links(self, page: str) -> Generator[str, None, None]:
        soup = BeautifulSoup(page, self._html_parser)
        table = soup.find("table")
        return (link["href"] for link in table.find_all("a"))

    def _filter_links(self, links: Iterable, station_ids: Iterable[str]) -> Iterator[str]:
        return filter(lambda link: any([link.startswith(station_id) for station_id in station_ids]), links)
