from pymongo import MongoClient
from gridfs import GridFS
import datetime
import os

class HTMLGridFSClient:
    def __init__(self,db_name="html_db"):
        HOST = os.getenv("MONGO_HOST","mongodb://root:example@localhost:27017")
        self.client = MongoClient(HOST)
        self.db = self.client[db_name]
        self.fs = GridFS(self.db)

    def save_html_file(self, file_path, metadata=None):
        """
        שומר קובץ HTML ב-GridFS עם מטה-דאטה אופציונלי.
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        filename = os.path.basename(file_path)
        with open(file_path, "rb") as f:
            file_id = self.fs.put(
                f,
                filename=filename,
                upload_date=datetime.datetime.utcnow(),
                metadata=metadata or {}
            )
        return file_id

    def get_html_file(self, file_id, output_path=None):
        """
        מחזיר תוכן HTML מקובץ GridFS לפי ID.
        אם נמסר output_path, כותב את הקובץ למערכת הקבצים.
        """
        file_data = self.fs.get(file_id)
        content = file_data.read()

        if output_path:
            with open(output_path, "wb") as f:
                f.write(content)

        return content

    def list_files(self):
        """
        מחזיר רשימת כל הקבצים שמורים עם ID ושם.
        """
        files = []
        for f in self.fs.find():
            files.append({
                "file_id": f._id,
                "filename": f.filename,
                "upload_date": f.upload_date,
                "metadata": f.metadata
            })
        return files

    def delete_file(self, file_id):
        """
        מוחק קובץ לפי ID.
        """
        self.fs.delete(file_id)
        return True

# ------------------------
# דוגמת שימוש
# ------------------------
if __name__ == "__main__":
    client = HTMLGridFSClient()

    # שמירת קובץ
    file_id = client.save_html_file("example.html", metadata={"tags": ["example", "test"]})
    print(f"Saved file with ID: {file_id}")

    # קריאת קובץ
    content = client.get_html_file(file_id)
    print(content.decode("utf-8"))

    # רשימת כל הקבצים
    for f in client.list_files():
        print(f)

    # מחיקת קובץ
    # client.delete_file(file_id)
