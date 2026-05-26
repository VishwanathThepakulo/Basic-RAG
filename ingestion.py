from dotenv import load_dotenv
import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, PyMongoError
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_core.documents import Document
import uuid 
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
        if not db_credentials:
            raise Exception("DB credentials not found")
        embedding_api_key = os.getenv("EMBEDDING_API_KEY")
        if not embedding_api_key:
            raise Exception("embeddings api key not found")
        self.client = MongoClient(db_credentials, serverSelectionTimeoutMS=2000)
        self.collection = self.client['RAG_Collection']['Searchable_TABLE']
        self.embedding_model = HuggingFaceEndpointEmbeddings(
            model="sentence-transformers/all-MiniLM-L6-v2",
            huggingfacehub_api_token=embedding_api_key,
        )
        
    def check_mongodb_connection(self):
        try:
            self.client.admin.command('ping')
            print("Success! Connected to MongoDB successfully.")
        except ServerSelectionTimeoutError as e:
            print("Connection Failed! Could not connect to MongoDB server.")
            print(f"Error details: {e}")   
        except PyMongoError as e:
            print(f"an mongoDB error occured: {e}")
        except Exception as e:
            print(f"an unexcepted error occured: {e}")
                
        
        
    def pdf_loader(self, file):
        documents = []
        document_id = str(uuid.uuid4())

        with fitz.open(file) as pdf:
            for page_number, page in enumerate(pdf):
                text = page.get_text()

                text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
                text = re.sub(r'\n\s*\n', '\n\n', text)
                document = Document(
                    page_content=text,
                    metadata = {
                        'document_id':document_id,
                        'source':file,
                        'page':page_number+1
                    }
                )
                documents.append(document)
        
        self.chunking(documents) 
        return documents
    
    def chunking(self, documents):

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 500,
            chunk_overlap = 100,
            separators=["\n\n", "\n", " ", ""], 
            add_start_index=True,
        )
        split_docs = text_splitter.split_documents(documents)

        texts = []
        metadatas = []

        for chunk_index, doc in enumerate(split_docs):
            
            
            doc.metadata['chunk_id']=(f"{doc.metadata['document_id']}__page__{doc.metadata['page']}__chunk__{chunk_index}")
            doc.metadata["chunk_index"] = chunk_index,
            # doc.metadata['start_index']:doc.metadata.get("start_index")
            
            texts.append(doc.page_content)  
            metadatas.append(doc.metadata)

        self.Create_Embeddings(texts,metadatas)
        return {
            'texts':texts,
            'metadatas':metadatas
        }
    
    def Create_Embeddings(self, chunks, metadatas):
        embeddings = self.embedding_model.embed_documents(chunks)
        logger.info("Successfully generated embeddings")
        # print(embeddings)
        docs_to_insert = []
        for text, meta, embd in zip(chunks, metadatas, embeddings):
            items = {
                "text":text,
                'embeddings':embd,
                **meta
            }
            docs_to_insert.append(items)
        self.Store_in_Vector_DB(docs_to_insert)
        return {
            "status":200,
            "embeddings": embeddings
        }
        
    
    
    def Store_in_Vector_DB(self, docs_to_insert):
        result = self.collection.insert_many(docs_to_insert)
        print(f"inserted_count:{len(result.inserted_ids)}")
        return {
            'status':200,
            "inserted_count":len(result.inserted_ids)
        }
        


    def query_embedding(self, query):
        query_embeddings = self.embedding_model.embed_query(query)
        return query_embeddings


    def Similarity_Search(self, embedded_query):
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "embedding",
                    "queryVector": embedded_query,
                    "numCandidates": 100,
                    "limit": 5
                }
            }
        ]

        results = self.collection.aggregate(pipeline)

        for doc in results:
            print(doc["name"])
        return results

    
    def Relevant_Chunks_Retrieved():
        pass
        
    def connection_close(self):
        self.client.close()
        
          






if __name__=='__main__':
    dbIngestion = db_ingestion()
    dbIngestion.check_mongodb_connection()
















































