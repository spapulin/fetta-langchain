# fetta-langchain

LangChain document loader that uses [fetta](https://github.com/spapulin/fetta) -
a tool that fetches web pages for assistants


## ⚡ Async-first

**`fetta-langchain` is async-only.** The loader implements `alazy_load`,
not `lazy_load`. Every fetch is awaited.

This is deliberate as `fetta` is async by design, and LangChain's
sync path would either block the event loop or require a separate
thread-based implementation. Agents, MCP servers, and FastAPI
backends all run async, and the loader fits that world.

If you're in a sync context, bridge it at your entry point:

```python
import asyncio
from fetta_langchain import FettaLoader

async def load():
    loader = FettaLoader(urls=["https://example.com"])
    return await loader.aload()

docs = asyncio.run(load())
```

Don't call `asyncio.run()` from inside an async function - that
raises `RuntimeError`. The bridge is for the *outermost* layer of
sync programs only.

## Install

`fetta-langchain` is not on PyPI yet. Install directly from GitHub.

### As a library

With uv (recommended):

    uv add "fetta-langchain @ git+https://github.com/spapulin/fetta-langchain.git"

With pip:

    pip install "fetta-langchain @ git+https://github.com/spapulin/fetta-langchain.git"

This pulls `fetta` and `langchain-core` automatically as dependencies.

For browser-based fetching, also install Chromium:

    # With uv
    uv run playwright install chromium --with-deps

    # With pip (venv activated)
    python -m playwright install chromium --with-deps

`--with-deps` installs system libraries and requires `sudo` on Linux.
On macOS, drop the flag. 

Skip this step entirely if you only use `HttpFetcher`.

### Development version

The latest unreleased code from `main`. May contain bugs, may
break without notice. Use only if you need a fix that hasn't
shipped to PyPI yet.

    uv add "fetta @ git+https://github.com/spapulin/fetta-langchain.git@main"
    pip install "fetta @ git+https://github.com/spapulin/fetta-langchain.git@main"

For reproducible installs, pin to a tag or commit:

    uv add "fetta @ git+https://github.com/spapulin/fetta-langchain.git@v0.1.0"

### Set up for development

#### With Docker

    git clone https://github.com/spapulin/fetta-langchain.git
    cd fetta

    make up      # build image, start container
    make sync    # install dependencies in the container
    make test    # run tests in the container

Playwright browsers and system libraries are baked into the image.

**Optional**: IDE autocompletion

PyCharm and other IDEs need a local Python interpreter for
autocompletion and "go to definition". Create a lightweight
host venv - runtime packages only, no dev tools, no browsers:

    # With uv
    uv venv
    uv pip install -e .

    # With pip
    python -m venv .venv
    source .venv/bin/activate
    pip install -e .

Point your IDE at `.venv/bin/python`.

Code still runs inside Docker (`make test`). The host venv is
only for the editor - it has no Playwright browsers and cannot
execute `BrowserFetcher`.

#### Without Docker

    git clone https://github.com/spapulin/fetta-langchain.git
    cd fetta

    uv sync --dev
    uv run playwright install chromium --with-deps
    uv run pytest


## Quickstart

The fastest way to try `fetta-langchain` is the Jupyter notebook:

    notebooks/quickstart.ipynb

It walks through:

- Loading documents with `FettaLoader` backed by `HttpFetcher`
- Loading documents with `FettaLoader` backed by `BrowserFetcher`
- Building a simple summarization chain with LangChain

### Running the notebook

With Docker (recommended):

    make jupyter

Then open http://localhost:8888 and navigate to `notebooks/quickstart.ipynb`.

Without Docker:

    uv run jupyter lab

## Requirements

- Python 3.12+
- Playwright browsers (Chromium) - only for `BrowserFetcher` and `SmartFetcher`
- Docker - only for development

## License

MIT — see [LICENSE](LICENSE)