from ingestion import db_ingestion
from fastapi import FastAPI
from pydantic import BaseModel

dbIngestion = db_ingestion()


app = FastAPI()
class validate_uploading_pdf(BaseModel):
    path:str

class ValidateQuery(BaseModel):
    query:str



@app.post('/document/ingestion/intoDB')
def db_ingestion_endpoint(uploading_path : validate_uploading_pdf):
    # user_pdf_input = input("Enter a pdf path : ")
    
    user_pdf_output = dbIngestion.pdf_loader(uploading_path.path)
    # for para in user_pdf_output:
    #     print("PARAGRAPH:")
    #     print(para)
    #     print("="*50)
    # print(user_pdf_output)
    return {"status": 200, 'length':user_pdf_output}


@app.post("/api/query")
def user_query(query : ValidateQuery):
    users_query_is = dbIngestion.query_embedding(query.query)
    similarity_search = dbIngestion.Similarity_Search(users_query_is)
    pass






if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",              
        host='localhost',
        port=9000
        # reload=True             
    )
