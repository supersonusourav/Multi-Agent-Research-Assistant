from dotenv import load_dotenv
# from langchain_mistralai import ChatMistralAI
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# llm = ChatMistralAI(
#     model_name="mistral-large-latest",
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
     temperature=0,
 )
