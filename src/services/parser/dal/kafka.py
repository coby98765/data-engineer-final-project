from kafka import KafkaProducer,KafkaConsumer
# from src.shared.logging.logger import Logger
import os
import json

# logger setup
# logger = Logger.get_logger(index="kafka_log",name="kafka_connection")
import logging

logging.basicConfig(
    level=logging.INFO,  # רמת לוג מינימלית שתירשם
    format='%(asctime)s - %(levelname)s - %(message)s',  # פורמט הודעה
    filename="logs.log")


logger = logging

class Kafka:
    def __init__(self,group_id):
        self.bootstrap_servers = os.getenv("KAFKA_HOST","localhost:9092")
        self.group_id = group_id
        self.producer = None
        self.consumer = None

    def create_producer(self):
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode("utf-8")
            )
            logger.info('Kafka.create_producer, connected to kafka PUB')
        except Exception as ex:
            logger.error(f"Kafka.create_producer, Error: {ex}")
            raise Exception(ex)

    def create_consumer(self,sub_topic):
        try:
            self.consumer = KafkaConsumer(
                sub_topic,
                bootstrap_servers=self.bootstrap_servers,
                group_id=self.group_id,
                value_deserializer=lambda v: json.loads(v.decode("utf-8"))
            )
            logger.info('Kafka.create_consumer connected to kafka SUB')
        except Exception as ex:
            logger.error(f"Kafka.create_consumer, Error: {ex}")
            raise Exception(ex)

    def pub(self, data, topic):
        try:
            self.producer.send(topic, value=data)
            logger.info(f"Kafka.pub, sent to topic: {topic}")
        except Exception as ex:
            logger.error(f"Kafka.pub, Error: {ex}")
            raise Exception(ex)

    def sub(self):
        try:
            for msg in self.consumer:
                logger.info('Kafka.sub, received report.')

                yield msg.value
            return
        except Exception as ex:
            logger.error(f"Kafka.sub, Error: {ex}")
            raise Exception(ex)
        finally:
            self.consumer.close()
            logger.info('Kafka.sub, consumer closed.')
