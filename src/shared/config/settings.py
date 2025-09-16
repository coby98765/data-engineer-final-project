# from pydantic import BaseSettings
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = "dev"
    MONGO_URI: str = "mongodb://mongo:27017"
    ELASTIC_URL: str = "http://elasticsearch:9200"
    KAFKA_BOOTSTRAP: str = "kafka:9092"
    HDFS_URL: str = "http://namenode:9870"
    API_BASE_URL: str = "http://api:8000"

    SCRAPER_URL: str = "http://scraper:8000"
    PARSER_URL: str = "http://parser:8000"
    EXPANDER_URL: str = "http://expander:8000"
    GEOCODER_URL: str = "http://geocoder:8000"
    INDEXER_URL: str = "http://indexer:8000"

    class Config :
        env_file = "../../../.env.example"

    # class Config:
    #     env_file = "../../../.env.local"


def get_settings() -> Settings:
    return Settings()  # pydantic קורא אוטומטית משתני סביבה

settings = get_settings()

print(settings.MONGO_URI)
