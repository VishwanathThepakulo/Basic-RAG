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
        self.api_key = os.environ.get('GROQ_API_KEY')
        if not self.api_key:
            logger.error("error from api key initilization")

    def query_to_llm(self,context,user_query):
        client = Groq()
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
            {
            "role": "system",
            "content": "Answer only from the provided context."
            },
            {
                "role": "user",
                "content": f"""
                Context:
                {context}

                Question:
                {user_query}
                """
            }
            ],
            temperature=1,
            max_completion_tokens=1024,
            # top_p=1,
            stream=True,
            # stop=None,
            # compound_custom={"tools":{"enabled_tools":["web_search","code_interpreter","visit_website"]}}
        )
        final_response = ""
        for chunk in completion:
            content = chunk.choices[0].delta.content or ""
            final_response += content
        return final_response
        






