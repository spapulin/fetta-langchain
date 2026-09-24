FROM mcr.microsoft.com/playwright/python:v1.63.0-jammy

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

ENV UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/home/pwuser/.venv \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_INSTALL_DIR=/usr/local/share/uv \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN mkdir -p /fetta /usr/local/share/uv && chmod 755 /usr/local/share/uv

# Playwright's official docs recommend a non-root user for scraping
# untrusted sites, and --ipc=host (set in compose) for Chromium.
# Note: User pwuser is UID 1000 that we need to create jupyter notebook
# in host browser
RUN chown -R pwuser:pwuser /app /fetta /usr/local/share/uv

USER pwuser

CMD ["sleep", "infinity"]