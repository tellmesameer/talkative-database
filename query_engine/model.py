# D:\AI_Project\talkative-database\query_engine\model.py
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model


load_dotenv()
def init_llm():
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] =  os.getenv("OPENAI_API_KEY", "")
        
    llm = init_chat_model("gpt-4o-mini", model_provider="openai")

    return llm 