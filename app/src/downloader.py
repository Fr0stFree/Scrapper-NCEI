import asyncio
from typing import AsyncGenerator, Final, Optional, Iterable

import aiohttp


class PageDownloader:
    ENCODING: Final[str] = "utf-8"

    def __init__(self, semaphore_limit: int = 5) -> None:
        self.semaphore: asyncio.Semaphore = asyncio.Semaphore(semaphore_limit)

    async def get_concurrently(self, urls: Iterable[str]) -> AsyncGenerator[str, None]:
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.create_task(self._get(url, session)) for url in urls]
            for task in asyncio.as_completed(tasks):
                try:
                    page: str = await task
                except Exception:
                    continue
                else:
                    yield page

    async def get(self, url: str, session: Optional[aiohttp.ClientSession] = None) -> str:
        if session is not None:
            return await self._get(url, session)

        async with aiohttp.ClientSession() as session:
            return await self._get(url, session)

    async def _get(self, url: str, session: aiohttp.ClientSession) -> str:
        async with self.semaphore:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.text(encoding=self.ENCODING)
