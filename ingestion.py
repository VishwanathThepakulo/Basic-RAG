from dotenv import load_dotenv
import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, PyMongoError
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEndpointEmbeddings
import fitz
import logging
import re
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    filename='app.log',
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

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
        self.embedding_model = HuggingFaceEndpointEmbeddings(
            model="sentence-transformers/all-MiniLM-L6-v2",
            huggingfacehub_api_token=embedding_api_key,
        )
        
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
                
        
        
    def pdf_loader(self, file):
        doc = fitz.open(file)
        text = ''
        for page in doc:
            text+=page.get_text()
        text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        # paragraph = text.split("\n\n")
        # cleaned_paragraph = []
        # for p in paragraph:
        #     if p.strip():
        #         cleaned_paragraph.append(p.strip())
        # paragraphs = cleaned_paragraph
        self.chunking(text)
        return text
    
    def chunking(self, text):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 200,
            separators=["\n\n", "\n", " ", ""], 
        )
        chunks = text_splitter.split_text(text)
        # print(f"====================================\n\n{chunks}\n\n=====================================================")
        # for chunk in chunks:
        #     print(chunk)
        #     print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        #     print()
        self.Create_Embeddings(chunks)
        return chunks
    
    def Create_Embeddings(self, chunks):
        embeddings = self.embedding_model.embed_documents(chunks)
        logger.info("Successfully generated embeddings")
        print(embeddings)
        return {
            "status":200,
            "embeddings": embeddings
        }
    
    def Store_in_Vector_DB():
        pass
    def Similarity_Search():
        pass
    
    def Relevant_Chunks_Retrieved():
        pass
        
    def connection_close(self):
        self.client.close()
        
          
if __name__=='__main__':
    dbIngestion = db_ingestion()
    dbIngestion.check_mongodb_connection()
















































