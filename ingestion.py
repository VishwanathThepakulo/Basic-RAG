from dotenv import load_dotenv
import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, PyMongoError
import fitz
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
        self.client = MongoClient(db_credentials, serverSelectionTimeoutMS=2000)
        
    def check_mongodb_connection(self):
        try:
            self.client.admin.command('ping')
            print("✅ Success! Connected to MongoDB successfully.")
        except ServerSelectionTimeoutError as e:
            print("❌ Connection Failed! Could not connect to MongoDB server.")
            print(f"Error details: {e}")   
        except PyMongoError as e:
            print(f"an mongoDB error occured: {e}")
        except Exception as e:
            print(f"an unexcepted error occured: {e}")
        finally:
            self.client.close()    
        
        
    def pdf_loader(file):
        doc = fitz.open(file)
        text = ''
        for page in doc:
            text+=page.get_text()
            
        paragraph = text.split("\n\n")
        cleaned_paragraph = []
        for p in paragraph:
            if p.strip():
                cleaned_paragraph.append(p.strip())
        paragraphs = cleaned_paragraph
        return paragraphs
        
        
        
          
if __name__=='__main__':
    dbIngestion = db_ingestion()
    dbIngestion.check_mongodb_connection()
















































