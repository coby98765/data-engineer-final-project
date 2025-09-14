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
