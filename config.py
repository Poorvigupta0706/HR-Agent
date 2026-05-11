import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.rate_limiters import InMemoryRateLimiter

load_dotenv()

rate_limiter = InMemoryRateLimiter(requests_per_second=0.4)

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
    rate_limiter=rate_limiter
)