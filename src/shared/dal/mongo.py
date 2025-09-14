from ..config import get_settings

from src.shared.logging.logger import Logger
from pymongo import MongoClient ,errors
import os

# logger setup
logger = Logger.get_logger(index="persister_log",name="persister.mongoDAL.py")


class MongoDAL:
    def __init__(self):
        self.DB_HOST = os.getenv("MONGO_HOST","mongodb://localhost:27017/")
        self.DB_NAME = os.getenv("MONGO_NAME","muezzin")
        self.DB_COLL = os.getenv("MONGO_REPORT_COLL", "podcasts_meta")
        client = None
        try:
            client = MongoClient(self.DB_HOST)
            logger.info(f'MongoDAL.init, connected to MongoDB.')
        except Exception as e:
            logger.error(f"MongoDAL.init, Error: {e}")
            raise
        finally:
            client.close()


    def load_report(self,report):
        client = None
        try:
            client = MongoClient(self.DB_HOST)
            mydb = client[self.DB_NAME]
            collection = mydb[self.DB_COLL]
            res = collection.insert_one(report)
            logger.info(f'MongoDAL.load_report, {res.inserted_id} added to mongoDB.')
            return res.inserted_id
        except errors.ServerSelectionTimeoutError as e:
            logger.error(f"MongoDAL.load_report, Server selection timeout: {e}")
            raise
        except errors.ConnectionFailure as e:
            logger.error(f"MongoDAL.load_report, Connection failed: {e}")
            raise
        except errors.ConfigurationError as e:
            logger.error(f"MongoDAL.load_report, Configuration error: {e}")
            raise
        except Exception as e:
            logger.error(f"MongoDAL.load_report, Unexpected error: {e}")
            raise
        finally:
            client.close()

