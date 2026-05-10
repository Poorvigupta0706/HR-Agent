import os
from dotenv import load_dotenv

from langchain_core.globals import set_llm_cache
from langchain_community.cache import SQLiteCache

from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
set_llm_cache(
    SQLiteCache(database_path=".langchain.db")
)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0
)
google_api_key = os.getenv("GOOGLE_API_KEY")

langsmith_api_key = os.getenv("LANGCHAIN_API_KEY")