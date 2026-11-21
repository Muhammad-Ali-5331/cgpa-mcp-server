from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import init_chat_model

LLM = init_chat_model(model="groq:openai/gpt-oss-20b")
