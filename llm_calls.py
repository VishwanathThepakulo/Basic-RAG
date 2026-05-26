import os
from groq import Groq
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    filename='llmlogs.log',
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class LLMCallings():
    def __init__(self):
        api_key = os.environ.get('GROQ_API_KEY')
        if not api_key:
            logger.error("error from api key initilization")

    def query_to_llm():
        pass





pipeline = [
    {
        "$vectorSearch": {
            "index": "vector_index",
            "path": "embedding",
            "queryVector": query_embedding,
            "numCandidates": 100,
            "limit": 5
        }
    }
]

results = collection.aggregate(pipeline)

for doc in results:
    print(doc["name"])






