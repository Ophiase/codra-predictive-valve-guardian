FROM ghcr.io/astral-sh/uv:python3.12-alpine

WORKDIR /app

# Pre-install dependencies
COPY pyproject.toml uv.lock /app/
RUN uv sync --frozen

# Copy the rest of the application code
COPY . /app

# ENV UV_LINK_MODE=copy
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

EXPOSE 8501

CMD ["sh", "-c", "uv run streamlit run src/dashboard/__main__.py --server.port=8501 --server.address=0.0.0.0"]
