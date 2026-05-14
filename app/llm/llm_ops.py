import os
from dotenv import load_dotenv
from openai import OpenAI
from ollama import chat

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

def make_ollama_call(inp : str , model : str = "mistral:7b"):
    response = chat(
        model=model,
        messages=[
            {'role' : 'system' , 'content' : "You are a helpful assistant."},
            {'role' : 'user' , 'content' : inp}]
    )
    return response.message.content