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

## Parser Service

### Overview
Parser Service extracts city information from HTML files, stores it in MongoDB, and sends relevant links or IDs to Kafka for downstream services.

### Components
- **Manager**: Reads HTML, parses city data, handles partial entries, and saves to MongoDB.
- **CityParser**: Extracts city name, status, and link from HTML rows.
- **Cleaning_city**: Helper class to clean and extract data from HTML.

## scraper_2

The service receives a url from Kafka in the topic "topic-to-parser-streets" 
(the address of the cities involved)

and the service extracts all the data from the website's html
and then stores the information in gridfs and sends the unique identifier in Kafka to the topic "topic-to-parser-streets"

## Expander Service

### Overview
Expander Service parses city streets and buildings from HTML files, saves data into MongoDB, and sends IDs to Kafka for other services.

### Components
- **Manager**: Parses streets from HTML and saves to MongoDB.
- **Manager_buildings**: Parses buildings for partial streets and saves to MongoDB.
- **CityParser**: Extracts street and city info from HTML.
- **building_Parser**: Extracts building numbers and status from street HTML.
- **Cleaning_html**: Helper classes to clean and extract data from HTML.

## Collaborators
[![Contributors](https://contrib.rocks/image?repo=coby98765/data-engineer-final-project)](https://github.com/coby98765/data-engineer-final-project/graphs/contributors)

Made with [contrib.rocks](https://contrib.rocks).

