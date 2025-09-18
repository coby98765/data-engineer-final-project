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

## geocoder

This service acts as a bridge between your data pipeline and geospatial visualization needs. It receives city IDs from `scraper_2`, fetches the corresponding city information from a MongoDB database, determines discount eligibility for each city, and generates a GeoJSON output using OSMnx. The resulting GeoJSON is color-coded to visually represent the discount eligibility status of each city.

### How It Works

1. **Input**: Receives a list of city IDs from the `scraper_2` service (via HTTP, message queue, or another interface).
2. **Data Retrieval**: For each city ID, queries MongoDB to retrieve detailed city information (e.g., name, coordinates, eligibility).
3. **Eligibility Check**: For each city, checks if it qualifies for a discount based on the relevant business logic/criteria.
4. **GeoJSON Generation**: Uses OSMnx to generate a GeoJSON representation of each city.
5. **Color Coding**: Colors each city in the GeoJSON according to its discount eligibility status:
    - **Eligible cities**: Marked with a distinct color (e.g., green).
    - **Non-eligible cities**: Marked with another color (e.g., red).
    - **Note:** In the generated GeoJSON, the `color` property is specified using the name of the color (e.g., `"green"`, `"red"`), **not** a hex code.
6. **Output**: Returns or stores the resulting color-coded GeoJSON for downstream visualization or mapping applications.
7. **GeoJSON File Creation**: The service creates and saves a GeoJSON file containing all the processed city features. This file can be used for mapping or further analysis.

### Example Workflow

```
[scraper_2] → [City Eligibility GeoJSON Service] → [MongoDB] → [OSMnx] → [GeoJSON Output] → [GeoJSON File]
```

### API/Integration

- **Input**: List of city IDs
- **Output**: GeoJSON file/object, with each city feature containing a `color` property (with color name) based on eligibility

### Dependencies

- Python 3.x
- [OSMnx](https://github.com/gboeing/osmnx)
- [PyMongo](https://pymongo.readthedocs.io/)
- Your preferred web framework (e.g., Flask, FastAPI) for service endpoints

### Example GeoJSON Feature

```json
{
  "type": "Feature",
  "properties": {
    "city_name": "Sample City",
    "eligible": true,
    "color": "green"
  },
  "geometry": {
    "type": "Polygon",
    "coordinates": [ ... ]
  }
}
```

### Customization

- **Eligibility Logic**: Adjust the logic for discount eligibility in your code as business requirements change.
- **Color Scheme**: Modify the color names in the service configuration to match your visualization needs.

### Usage

1. Start the service.
2. Send a request or message with a list of city IDs.
3. Receive or fetch the resulting color-coded GeoJSON for mapping or further processing.
4. The service will create and save a GeoJSON file with all city features, which can be used directly in mapping tools or for further geospatial analysis.

---

For more details on endpoints, configuration, or customization, please refer to the main documentation or source code.

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

