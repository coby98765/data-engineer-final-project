#!/usr/bin/env bash
set -euo pipefail

REPO_NAME="${1:-ravkav-geo}"
echo "Scaffolding repo: ${REPO_NAME}"
mkdir -p "$REPO_NAME"
cd "$REPO_NAME"

# -------------------
# Root files
# -------------------
cat > README.md <<'EOF'
# RavKav Geo — Monorepo Skeleton

Monorepo לפרויקט Data Engineering:
- Streamlit Client (Public UI)
- Streamlit Admin (שליטה/סטטוסים)
- FastAPI (API)
- Services: scraper, parser, expander, geocoder, indexer
- Shared lib: config, logging, DAL (Mongo/ES/HDFS/Kafka), utilities
- Infra: docker-compose.dev, K8s manifests, GitHub Actions

## פקודות מהירות
- `make dev-up` — מרימות תלויות (Kafka/Mongo/ES/HDFS) + שירותים בסיסיים.
- `make dev-down`
- `make test`
- `make fmt` / `make lint`
EOF

cat > .env.example <<'EOF'
# Example env
ENV=dev
MONGO_URI=mongodb://mongo:27017
ELASTIC_URL=http://elasticsearch:9200
KAFKA_BOOTSTRAP=kafka:9092
HDFS_URL=http://namenode:9870
API_BASE_URL=http://api:8000
EOF

cat > Makefile <<'EOF'
SHELL := /bin/bash
.PHONY: dev-up dev-down test fmt lint

dev-up:
\tdocker compose -f infra/docker/compose.dev.yml up -d --build

dev-down:
\tdocker compose -f infra/docker/compose.dev.yml down -v

test:
\tpytest -q

fmt:
\trufflehog --help >/dev/null 2>&1 || true
\tblack src tests

lint:
\tflake8 src tests || true
EOF

cat > pyproject.toml <<'EOF'
[project]
name = "ravkav-geo"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
  "fastapi",
  "uvicorn[standard]",
  "streamlit",
  "pydantic>=2",
  "pandas",
  "beautifulsoup4",
  "lxml",
  "requests",
  "pymongo",
  "elasticsearch>=8",
  "confluent-kafka",
  "hdfs",
  "python-dotenv",
  "structlog",
  "folium",
]

[tool.black]
line-length = 100

[tool.flake8]
max-line-length = 100
extend-ignore = E203
EOF

# -------------------
# Source tree
# -------------------
mkdir -p src/services/{app,admin,api,scraper,parser,expander,geocoder,indexer}
mkdir -p src/shared/{config,logging,dal,clients,messaging,utils,api_template}
touch src/__init__.py

# -------------------
# Shared: settings + logger
# -------------------
cat > src/shared/config/__init__.py <<'EOF'
from .settings import get_settings, Settings
__all__ = ["get_settings", "Settings"]
EOF

cat > src/shared/config/settings.py <<'EOF'
from pydantic import BaseSettings

class Settings(BaseSettings):
    ENV: str = "dev"
    MONGO_URI: str = "mongodb://mongo:27017"
    ELASTIC_URL: str = "http://elasticsearch:9200"
    KAFKA_BOOTSTRAP: str = "kafka:9092"
    HDFS_URL: str = "http://namenode:9870"
    API_BASE_URL: str = "http://api:8000"

def get_settings() -> Settings:
    return Settings()  # pydantic קורא אוטומטית משתני סביבה
EOF

cat > src/shared/logging/__init__.py <<'EOF'
from .logger import get_logger
__all__ = ["get_logger"]
EOF

cat > src/shared/logging/logger.py <<'EOF'
import structlog
import logging
import os

def get_logger(service: str):
    logging.basicConfig(
        format="%(message)s",
        level=os.getenv("LOG_LEVEL","INFO"),
    )
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.JSONRenderer(),
        ]
    )
    log = structlog.get_logger().bind(service=service, env=os.getenv("ENV","dev"))
    return log
EOF

# -------------------
# Shared: DALs
# -------------------
cat > src/shared/dal/__init__.py <<'EOF'
from .mongo import get_mongo
from .elastic import get_es
from .kafka import get_producer, get_consumer
from .hdfs import get_hdfs_client
__all__ = ["get_mongo", "get_es", "get_producer", "get_consumer", "get_hdfs_client"]
EOF

cat > src/shared/dal/mongo.py <<'EOF'
from pymongo import MongoClient
from ..config import get_settings

_client = None
def get_mongo() -> MongoClient:
    global _client
    if not _client:
        uri = get_settings().MONGO_URI
        _client = MongoClient(uri)
    return _client
EOF

cat > src/shared/dal/elastic.py <<'EOF'
from elasticsearch import Elasticsearch
from ..config import get_settings

_es = None
def get_es() -> Elasticsearch:
    global _es
    if not _es:
        url = get_settings().ELASTIC_URL
        _es = Elasticsearch(url)
    return _es
EOF

cat > src/shared/dal/kafka.py <<'EOF'
from confluent_kafka import Producer, Consumer
from ..config import get_settings

def get_producer():
    return Producer({"bootstrap.servers": get_settings().KAFKA_BOOTSTRAP})

def get_consumer(group_id: str, topics: list[str]):
    c = Consumer({
        "bootstrap.servers": get_settings().KAFKA_BOOTSTRAP,
        "group.id": group_id,
        "auto.offset.reset": "earliest",
    })
    c.subscribe(topics)
    return c
EOF

cat > src/shared/dal/hdfs.py <<'EOF'
from hdfs import InsecureClient
from ..config import get_settings

_client = None
def get_hdfs_client():
    global _client
    if not _client:
        _client = InsecureClient(get_settings().HDFS_URL, user="hdfs")
    return _client
EOF

# -------------------
# Shared: clients/messaging/utils
# -------------------
cat > src/shared/clients/__init__.py <<'EOF'
from .geocoders import GeocoderClient
from .http import http_get_json
__all__ = ["GeocoderClient", "http_get_json"]
EOF

cat > src/shared/clients/http.py <<'EOF'
import time, requests

def http_get_json(url: str, params=None, timeout=20, retries=2):
    for i in range(retries+1):
        r = requests.get(url, params=params, timeout=timeout)
        if r.ok:
            return r.json()
        time.sleep(1)
    r.raise_for_status()
EOF

cat > src/shared/clients/geocoders.py <<'EOF'
from .http import http_get_json

class GeocoderClient:
    def __init__(self, provider: str = "osm"):
        self.provider = provider

    def geocode(self, query: str):
        if self.provider == "osm":
            url = "https://nominatim.openstreetmap.org/search"
            js = http_get_json(url, params={"q": query, "format": "json", "limit": 1})
            if js:
                hit = js[0]
                return {"lat": float(hit["lat"]), "lon": float(hit["lon"]), "score": 1.0, "provider": "osm"}
        # TODO: arcgis/govmap providers
        return None
EOF

cat > src/shared/messaging/__init__.py <<'EOF'
from .topics import Topics
from .schemas import ParsedRule, DerivedAddress, EnrichedAddress
__all__ = ["Topics", "ParsedRule", "DerivedAddress", "EnrichedAddress"]
EOF

cat > src/shared/messaging/topics.py <<'EOF'
class Topics:
    PARSED_RULES = "parsed.rules"
    DERIVED_ADDRESSES = "derived.addresses"
    ENRICHED_ADDRESSES = "enriched.addresses"
EOF

cat > src/shared/messaging/schemas.py <<'EOF'
from pydantic import BaseModel, Field
from typing import Optional, List

class ParsedRule(BaseModel):
    locality: str
    street: str
    rule: str  # ALL_INCLUDED | ALL_EXCLUDED | PARTIAL_NUMBERS
    included_tokens: List[str] = []
    excluded_tokens: List[str] = []
    source_url: Optional[str] = None

class DerivedAddress(BaseModel):
    locality: str
    street: str
    house_number: int
    eligibility_rule: str

class EnrichedAddress(BaseModel):
    locality: str
    street: str
    house_number: int
    eligible: bool
    eligibility_rule: str
    lat: float
    lon: float
    score: float = 1.0
    provider: str = "osm"
EOF

cat > src/shared/utils/__init__.py <<'EOF'
from .html_parse import parse_html_to_rules
from .house_tokens import expand_tokens
from .geojson import to_point_feature
from .timeit import timeit
__all__ = ["parse_html_to_rules", "expand_tokens", "to_point_feature", "timeit"]
EOF

cat > src/shared/utils/html_parse.py <<'EOF'
# placeholder: הפונקציה תקרא HTML ותחזיר רשימת ParsedRule dicts
def parse_html_to_rules(html: str) -> list[dict]:
    return []
EOF

cat > src/shared/utils/house_tokens.py <<'EOF'
# placeholder: הרחבת טווחים/זוגיים/אי-זוגיים
def expand_tokens(tokens: list[str]) -> list[int]:
    return []
EOF

cat > src/shared/utils/geojson.py <<'EOF'
def to_point_feature(lat: float, lon: float, props: dict):
    return {"type":"Feature","geometry":{"type":"Point","coordinates":[lon,lat]},"properties":props}
EOF

cat > src/shared/utils/timeit.py <<'EOF'
import time
from contextlib import contextmanager

@contextmanager
def timeit(label="block"):
    t0 = time.time()
    yield
    dt = (time.time()-t0)*1000
    print(f"[timeit] {label}: {dt:.1f} ms")
EOF

# -------------------
# Shared: API template (base)
# -------------------
cat > src/shared/api_template/__init__.py <<'EOF'
from .base_service import build_service_app
__all__ = ["build_service_app"]
EOF

cat > src/shared/api_template/base_service.py <<'EOF'
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Callable, Optional
from ..logging import get_logger

class StartRequest(BaseModel):
    params: dict | None = None

def build_service_app(service_name: str, run_once: Callable[[], None]):
    app = FastAPI(title=f"{service_name} service")
    log = get_logger(service_name)
    state = {"status":"idle","last_error":None}

    @app.get("/status")
    def status():
        return state

    @app.post("/start")
    def start(req: StartRequest):
        if state["status"] == "running":
            return {"ok": False, "msg": "already running"}
        state["status"] = "running"
        state["last_error"] = None
        try:
            run_once()
            state["status"] = "idle"
            return {"ok": True}
        except Exception as e:
            log.error("run_once_failed", error=str(e))
            state["status"] = "error"
            state["last_error"] = str(e)
            return {"ok": False, "error": str(e)}

    return app
EOF

# -------------------
# Services: API (FastAPI)
# -------------------
cat > src/services/api/app.py <<'EOF'
from fastapi import FastAPI, Query
from typing import Optional
from src.shared.dal.elastic import get_es

app = FastAPI(title="Public API")

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.get("/search")
def search(locality: str, street: str, house: Optional[int] = Query(None)):
    es = get_es()
    must = [{"term":{"locality.keyword": locality}}, {"term":{"street.keyword": street}}]
    if house is not None:
        must.append({"term":{"house_number": house}})
    body = {"query":{"bool":{"must": must}}, "size": 1}
    res = es.search(index="eligibility_v1", body=body)
    hits = res.get("hits",{}).get("hits",[])
    if not hits:
        return {"found": False}
    doc = hits[0]["_source"]
    return {"found": True, "eligible": doc.get("eligible"), "lat": doc.get("lat"), "lon": doc.get("lon")}
EOF

# -------------------
# Services: Streamlit Client (Public)
# -------------------
cat > src/services/app/app.py <<'EOF'
import os, requests, streamlit as st

API = os.getenv("API_BASE_URL","http://api:8000")
st.set_page_config(page_title="RavKav Geo", layout="wide")

st.title("RavKav Geo — חיפוש זכאות")
locality = st.text_input("יישוב")
street = st.text_input("רחוב")
house = st.number_input("מספר בית", min_value=0, step=1)

if st.button("חפש"):
    params = {"locality": locality, "street": street}
    if house:
        params["house"] = int(house)
    r = requests.get(f"{API}/search", params=params, timeout=20)
    if r.ok:
        data = r.json()
        st.json(data)
    else:
        st.error(f"API error: {r.status_code}")
EOF

# -------------------
# Services: Streamlit Admin
# -------------------
cat > src/services/admin/app.py <<'EOF'
import os, requests, streamlit as st

SERVICES = {
    "scraper": os.getenv("SCRAPER_URL","http://scraper:8000"),
    "parser":  os.getenv("PARSER_URL","http://parser:8000"),
    "expander":os.getenv("EXPANDER_URL","http://expander:8000"),
    "geocoder":os.getenv("GEOCODER_URL","http://geocoder:8000"),
    "indexer": os.getenv("INDEXER_URL","http://indexer:8000"),
}

st.set_page_config(page_title="Admin", layout="wide")
st.title("Pipeline Admin")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Start Jobs")
    for name, base in SERVICES.items():
        if st.button(f"Run {name}"):
            try:
                r = requests.post(f"{base}/start", json={"params": {}}, timeout=10)
                st.write(name, r.json())
            except Exception as e:
                st.error(f"{name} start failed: {e}")

with col2:
    st.subheader("Status")
    for name, base in SERVICES.items():
        try:
            r = requests.get(f"{base}/status", timeout=5)
            st.write(name, r.json())
        except Exception as e:
            st.error(f"{name} status failed: {e}")
EOF

# -------------------
# Services: Skeletons for pipeline services using base template
# -------------------
for svc in scraper parser expander geocoder indexer; do
  cat > "src/services/${svc}/service.py" <<'EOF'
def run_once():
    # TODO: business logic for this service
    print("running job once...")
EOF
  cat > "src/services/${svc}/app.py" <<EOF
from src.shared.api_template import build_service_app
from .service import run_once

app = build_service_app(service_name="${svc}", run_once=run_once)
EOF
done

# -------------------
# Tests
# -------------------
mkdir -p tests/unit tests/integration
cat > tests/unit/test_smoke.py <<'EOF'
def test_smoke():
    assert True
EOF

# -------------------
# Infra: Docker & Compose
# -------------------
mkdir -p infra/docker infra/k8s/{services,}
cat > infra/docker/base-python.Dockerfile <<'EOF'
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
EOF

cat > infra/docker/service.Dockerfile <<'EOF'
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
EOF

cat > infra/docker/compose.dev.yml <<'EOF'
services:
  # Infra
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment: { ZOOKEEPER_CLIENT_PORT: 2181, ZOOKEEPER_TICK_TIME: 2000 }
    ports: [ "2181:2181" ]

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    depends_on: [ zookeeper ]
    environment:
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    ports: [ "9092:9092" ]

  mongo:
    image: mongo:6
    ports: [ "27017:27017" ]

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.14.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    ports: [ "9200:9200" ]

  namenode:
    image: bigdatahub/hadoop-namenode:3.3.6
    environment:
      CLUSTER_NAME: "local"
    ports: [ "9870:9870" ]
    volumes:
      - hadoop_namenode:/hadoop/dfs/name
  datanode:
    image: bigdatahub/hadoop-datanode:3.3.6
    environment:
      SERVICE_PRECONDITION: "namenode:9870"
    ports: [ "9864:9864" ]
    volumes:
      - hadoop_datanode:/hadoop/dfs/data
    depends_on: [ namenode ]

  # API (public)
  api:
    build:
      context: ../..
      dockerfile: infra/docker/service.Dockerfile
      args: { SERVICE: api }
    environment:
      - ELASTIC_URL=http://elasticsearch:9200
    depends_on: [ elasticsearch ]
    ports: [ "8000:8000" ]

  # Streamlit public app
  app:
    build:
      context: ../..
      dockerfile: infra/docker/service.Dockerfile
      args: { SERVICE: app }
    command: ["streamlit","run","src/services/app/app.py","--server.port=8501","--server.address=0.0.0.0"]
    environment:
      - API_BASE_URL=http://api:8000
    depends_on: [ api ]
    ports: [ "8501:8501" ]

  # Streamlit admin
  admin:
    build:
      context: ../..
      dockerfile: infra/docker/service.Dockerfile
      args: { SERVICE: admin }
    command: ["streamlit","run","src/services/admin/app.py","--server.port=8502","--server.address=0.0.0.0"]
    depends_on: [ api ]
    ports: [ "8502:8502" ]

  # Skeleton service containers (expose 800x)
  scraper:
    build:
      context: ../..
      dockerfile: infra/docker/service.Dockerfile
      args: { SERVICE: scraper }
    command: ["uvicorn","src.services.scraper.app:app","--host","0.0.0.0","--port","8001"]
    ports: [ "8001:8001" ]

  parser:
    build:
      context: ../..
      dockerfile: infra/docker/service.Dockerfile
      args: { SERVICE: parser }
    command: ["uvicorn","src.services.parser.app:app","--host","0.0.0.0","--port","8002"]
    ports: [ "8002:8002" ]

  expander:
    build:
      context: ../..
      dockerfile: infra/docker/service.Dockerfile
    args: { SERVICE: expander }
    command: ["uvicorn","src.services.expander.app:app","--host","0.0.0.0","--port","8003"]
    ports: [ "8003:8003" ]

  geocoder:
    build:
      context: ../..
      dockerfile: infra/docker/service.Dockerfile
      args: { SERVICE: geocoder }
    command: ["uvicorn","src.services.geocoder.app:app","--host","0.0.0.0","--port","8004"]
    ports: [ "8004:8004" ]

  indexer:
    build:
      context: ../..
      dockerfile: infra/docker/service.Dockerfile
      args: { SERVICE: indexer }
    command: ["uvicorn","src.services.indexer.app:app","--host","0.0.0.0","--port","8005"]
    ports: [ "8005:8005" ]

volumes:
  hadoop_namenode:
  hadoop_datanode:
EOF

# -------------------
# K8s placeholders
# -------------------
cat > infra/k8s/namespaces.yaml <<'EOF'
apiVersion: v1
kind: Namespace
metadata:
  name: ravkav-geo-dev
EOF

for s in api app admin scraper parser expander geocoder indexer; do
cat > "infra/k8s/services/${s}.yaml" <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${s}
  namespace: ravkav-geo-dev
spec:
  replicas: 1
  selector: { matchLabels: { app: ${s} } }
  template:
    metadata: { labels: { app: ${s} } }
    spec:
      containers:
        - name: ${s}
          image: ghcr.io/your-org/${s}:dev
          ports: [ { containerPort: 8000 } ]
---
apiVersion: v1
kind: Service
metadata:
  name: ${s}
  namespace: ravkav-geo-dev
spec:
  selector: { app: ${s} }
  ports:
    - name: http
      port: 80
      targetPort: 8000
EOF
done

echo "Done. Next steps:"
echo "1) cp .env.example .env"
echo "2) make dev-up   # ירים תלויות ושירותים בסיסיים"
echo "3) פתח: http://localhost:8501 (Client), http://localhost:8502 (Admin), http://localhost:8000/docs (API)"
