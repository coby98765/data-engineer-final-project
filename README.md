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


## scraper

The service receives a URL and extracts all the information from the website's HTML, stores the data in GridFS and sends the unique identifier in Kafka to the topic "topic-to-parser"


## scraper_2

The service receives a url from Kafka in the topic "topic-to-parser-streets" 
(the address of the cities involved)

and the service extracts all the data from the website's html
and then stores the information in gridfs and sends the unique identifier in Kafka to the topic "topic-to-parser-streets"

## Collaborators
[![Contributors](https://contrib.rocks/image?repo=coby98765/data-engineer-final-project)](https://github.com/coby98765/data-engineer-final-project/graphs/contributors)

Made with [contrib.rocks](https://contrib.rocks).

