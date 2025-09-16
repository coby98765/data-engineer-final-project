# Expander Service

## Overview
Expander Service parses city streets and buildings from HTML files, saves data into MongoDB, and sends IDs to Kafka for other services.

## Components
- **Manager**: Parses streets from HTML and saves to MongoDB.
- **Manager_buildings**: Parses buildings for partial streets and saves to MongoDB.
- **CityParser**: Extracts street and city info from HTML.
- **building_Parser**: Extracts building numbers and status from street HTML.
- **Cleaning_html**: Helper classes to clean and extract data from HTML.

## Technologies
- Python, BeautifulSoup, MongoDB, Kafka, FastAPI

## Running the Service
```bash
python src/services/expander/app.py
```
- API runs on `http://0.0.0.0:8001`
- Kafka and MongoDB should be running.

## Notes
- Handles partial streets to expand to buildings.
- HTML structure changes may require updating Cleaning_html classes.