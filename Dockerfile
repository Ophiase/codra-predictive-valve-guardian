FROM ghcr.io/astral-sh/uv:python3.12-bookworm

WORKDIR /app
COPY . /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV UV_LINK_MODE=copy
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

RUN uv sync --frozen

EXPOSE 8501

CMD ["sh", "-c", "uv run streamlit run dashboard/app.py --server.port=8501 --server.address=0.0.0.0"]
