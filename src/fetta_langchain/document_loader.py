import asyncio
import json
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
            preserve_order: bool = True,
            include_sections: tuple[str, ...] = ("metadata", "html"),
            max_concurrency: int = 5
    ) -> None:
        self.urls = [urls] if isinstance(urls, str) else urls
        self._fetcher = fetcher
        self._fetch_kwargs = fetch_kwargs or {}
        if include_sections:
            self._fetch_kwargs.update({"include": include_sections})
        self._preserve_order = preserve_order
        self._include_sections = include_sections
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
                content = []
                if "metadata" in self._include_sections:
                    content.append(
                        json.dumps(
                            page.content.metadata,
                            ensure_ascii=False,
                            default=str
                        )
                    )
                if "html" in self._include_sections:
                    content.append(page.content.html)
                if "text" in self._include_sections:
                    content.append(page.content.text)

                return Document(
                    page_content="\n\n".join(content),
                    metadata={
                        "url": page.url,
                        "icon": page.icon,
                        "title": page.title,
                        "description": page.description,
                        "status": page.status
                    }
                )

        tasks = [asyncio.create_task(fetch_page(u)) for u in self.urls]
        if self._preserve_order:
            for t in tasks:
                yield await t
        else:
            for coro in asyncio.as_completed(tasks):
                yield await coro