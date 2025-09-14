ARG SERVICE=api
FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir fastapi uvicorn[standard] streamlit pydantic pandas requests
COPY src /app/src
ENV PYTHONPATH=/app
EXPOSE 8000
CMD ["uvicorn","src.services.api.app:app","--host","0.0.0.0","--port","8000"]
