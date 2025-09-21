# Installing uv
FROM python:3.12-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Installing a project
ADD . .

# Start project
CMD ["uv", "run", "-m", "sferum_bot"]
