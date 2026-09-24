import asyncio
from typing import AsyncIterator, Iterator

from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document

from fetta import FetcherProtocol, HttpFetcher


class FettaLoader(BaseLoader):
    """
    Load web pages as LangChain Documents via any fetta fetcher.
    """

    def __init__(
            self,
            urls: str | list[str],
            fetcher: FetcherProtocol | None = None,
            *,
            fetch_kwargs: dict = None,
            max_concurrency: int = 5
    ) -> None:
        self.urls = [urls] if isinstance(urls, str) else list(set(urls))
        self._fetcher = fetcher
        self._fetch_kwargs = fetch_kwargs or {}
        self._max_concurrency = max_concurrency

    def lazy_load(self) -> Iterator[Document]:
        raise NotImplementedError(
            "FettaLoader is async-only. Use aload() or alazy_load()."
        )

    async def alazy_load(self) -> AsyncIterator[Document]:
        if self._fetcher is not None:
            async for doc in self._load_with(self._fetcher, self._max_concurrency):
                yield doc
        else:
            async with HttpFetcher() as fetcher:
                async for doc in self._load_with(fetcher, self._max_concurrency):
                    yield doc

    async def _load_with(
            self,
            fetcher: FetcherProtocol,
            max_concurrency: int
    ) -> AsyncIterator[Document]:
        sem = asyncio.Semaphore(max_concurrency)

        async def fetch_page(url: str) -> Document:
            async with sem:
                page = await fetcher.fetch(url, **self._fetch_kwargs)
                return Document(
                    page_content=page.text,
                    metadata={
                        "source": page.url,
                        "title": page.title,
                        "status": page.status
                    }
                )

        tasks = [asyncio.create_task(fetch_page(u)) for u in self.urls]
        # Note: We preserve order that matches urls
        for t in tasks:
            yield await t
