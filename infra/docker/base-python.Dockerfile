FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY pyproject.toml /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r <(python - <<PY
import tomllib,sys
data=tomllib.load(open("pyproject.toml","rb"))
print("\n".join(data.get("project",{}).get("dependencies",[])))
PY
)
COPY src /app/src
ENV PYTHONPATH=/app
