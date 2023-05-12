import asyncio
from typing import AsyncGenerator, Final, Optional, Iterable

import aiohttp


class PageDownloader:
    ENCODING: Final[str] = "utf-8"
    semaphore: asyncio.Semaphore = asyncio.Semaphore(5)

    @classmethod
    async def get_concurrently(cls, urls: Iterable[str]) -> AsyncGenerator[str, None]:
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.create_task(cls._get(url, session)) for url in urls]
            for task in asyncio.as_completed(tasks):
                try:
                    page: str = await task
                except Exception:
                    continue
                else:
                    yield page

    @classmethod
    async def get(cls, url: str, session: Optional[aiohttp.ClientSession] = None) -> str:
        if session is not None:
            return await cls._get(url, session)

        async with aiohttp.ClientSession() as session:
            return await cls._get(url, session)

    @classmethod
    async def _get(cls, url: str, session: aiohttp.ClientSession) -> str:
        async with cls.semaphore:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.text(encoding=cls.ENCODING)
