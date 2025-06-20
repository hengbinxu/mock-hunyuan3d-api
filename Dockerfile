FROM python:3.12.6-slim-bullseye

LABEL maintainer="developer" version="1.0.0"

ARG API_PORT=8080
ENV API_PORT=${API_PORT}

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:0.5.13 /uv /uvx /bin/

# Copy the application into the container.
COPY . /app

# Install the application dependencies.
WORKDIR /app
RUN uv sync --frozen --no-cache

# Run the application.
CMD ["uv", "run", "fastapi", "run", "main.py"]