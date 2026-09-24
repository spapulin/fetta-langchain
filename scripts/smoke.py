import asyncio

from fetta_langchain import FettaLoader


async def main() -> None:

    loader = FettaLoader(urls="https://yahoo.com")
    docs = await loader.aload()

    print(f"Loaded {len(docs)} document(s)")
    print(f"Source:  {docs[0].metadata['source']}")
    print(f"Title:   {docs[0].metadata['title']}")
    print(f"Status:  {docs[0].metadata['status']}")
    print(f"Content: {docs[0].page_content[:200]}")


if __name__ == "__main__":
    asyncio.run(main())