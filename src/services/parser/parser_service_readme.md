# Parser Service

## Overview
Parser Service extracts city information from HTML files, stores it in MongoDB, and sends relevant links or IDs to Kafka for downstream services.

## Components
- **Manager**: Reads HTML, parses city data, handles partial entries, and saves to MongoDB.
- **CityParser**: Extracts city name, status, and link from HTML rows.
- **Cleaning_city**: Helper class to clean and extract data from HTML.

## Technologies
- Python, BeautifulSoup, MongoDB, Kafka, FastAPI

## Running the Service
```bash
python src/services/parser/app.py
```
- API runs on `http://0.0.0.0:8003`
- Requires Kafka and MongoDB to be running.

## Notes
- Handles partial city entries and sends links to Kafka for further processing.
- HTML structure changes may require updating `Cleaning_city` class.