from dotenv import load_dotenv
import os
from pymongo import MongoClient
load_dotenv()





class db_ingestion():
    def init(self):
        db_credentials = os.getenv("DB_CREDENTIALS")      
        if not db_credentials:
            raise("DB credentials not found")
        embedding_api_key = os.getenv("EMBEDDING_API_KEY")
        if not embedding_api_key:
            raise("embeddings api key not found")
          
















































