from src.shared.logging.logger import Logger
from pymongo import MongoClient, errors
from bson import ObjectId
import gridfs



# logger setup
logger = Logger.get_logger(index="persister_log",name="persister.mongoDAL.py")



class MongoDAL:
    def __init__(self, uri="mongodb://localhost:27017", db_name="files_db"):
        try:
            self.client = MongoClient(uri)
            self.db = self.client[db_name]
            self.fs = gridfs.GridFS(self.db)
            logger.info("Connected to MongoDB successfully.")
        except errors.PyMongoError as e:
            logger.error("Error connecting to MongoDB: %s", e)
            raise

    # Insert file (returns id)
    def insert_file(self, file_path: str) -> str:
        try:
            with open(file_path, "rb") as f:
                file_id = self.fs.put(f)
            logger.info("File inserted successfully. ID=%s", file_id)
            return str(file_id)
        except (OSError, errors.PyMongoError) as e:
            logger.error("Error inserting file: %s", e)
            return ""

    # Get file by id
    def get_file(self, file_id: str, dest_path: str):
        try:
            grid_out = self.fs.get(ObjectId(file_id))
            with open(dest_path, "wb") as f:
                f.write(grid_out.read())
            logger.info("File retrieved successfully. ID=%s", file_id)
        except (OSError, errors.PyMongoError) as e:
            logger.error("Error retrieving file (ID=%s): %s", file_id, e)


    def insert_document(self, collection: str, data: dict) -> list:
        """
        Insert a simple document into a collection (without GridFS).
        Returns the inserted document id.
        """
        try:
            result = self.db[collection].insert_many(data)
            logger.info("Document inserted successfully. ID=%s", result)
            ids_as_strings = [str(_id) for _id in result.inserted_ids]
            return ids_as_strings
        except errors.PyMongoError as e:
            logger.error("Error inserting document: %s", e)
            return []


    def get_document(self, collection: str, doc_id: str) -> dict:
        """
        Retrieve a simple document from a collection by id.
        Returns the document or {} if not found.
        """
        try:
            doc = self.db[collection].find_one({"_id": ObjectId(doc_id)})
            if doc:
                logger.info("Document retrieved successfully. ID=%s", doc_id)
                return doc
            else:
                logger.warning("Document not found. ID=%s", doc_id)
                return {}
        except errors.PyMongoError as e:
            logger.error("Error retrieving document (ID=%s): %s", doc_id, e)
            return {}


    def get_all_document(self, collection: str, id_list: list) -> list:
        """
        Retrieve a simple document from a collection by id.
        Returns the document or {} if not found.
        """
        try:
            object_ids = [ObjectId(id_str) for id_str in id_list]

            documents = self.db[collection].find({"_id": {"$in": object_ids}})
            docs_list = list(documents)
            if docs_list:
                logger.info("Document retrieved successfully. ID=%s", docs_list)
                return docs_list
            else:
                logger.warning("Document not found. ID=%s", docs_list)
                return []
        except errors.PyMongoError as e:
            logger.error("Error retrieving document (ID=%s): %s", e)
            return []

