from dotenv import load_dotenv
import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
load_dotenv()





class db_ingestion():
    def __init__(self):
        db_credentials = os.getenv("DB_CREDENTIALS")
        print(db_credentials)      
        if not db_credentials:
            raise Exception("DB credentials not found")
        embedding_api_key = os.getenv("EMBEDDING_API_KEY")
        print(embedding_api_key)
        if not embedding_api_key:
            raise Exception("embeddings api key not found")
        self.client = MongoClient(db_credentials)
        
    def check_mongodb_connection(self):
        try:
            self.client.admin.command('ping')
            print("✅ Success! Connected to MongoDB successfully.")
        except ServerSelectionTimeoutError as e:
            print("❌ Connection Failed! Could not connect to MongoDB server.")
            print(f"Error details: {e}")   
        except Exception as e:
            print(f"an unexcepted error occured: {e}")
        finally:
            self.client.close()    
        
        
          
if __name__=='__main__':
    dbIngestion = db_ingestion()
    dbIngestion.check_mongodb_connection()
















































