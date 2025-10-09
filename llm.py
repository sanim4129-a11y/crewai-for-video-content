from langchain_google_genai import ChatGoogleGenerativeAI
import os

gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro-latest",
    api_key=os.environ.get("GOOGLE_API_KEY")
)
