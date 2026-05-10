import os
from dotenv import load_dotenv
from langchain_core.globals import set_llm_cache
from langchain_community.cache import SQLiteCache
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()
set_llm_cache(SQLiteCache(database_path=".langchain.db"))
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = "HR-ATS-System"
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0
)