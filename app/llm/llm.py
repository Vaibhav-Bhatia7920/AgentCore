import ollama
from ollama import chat
from app.prompt.prompt_builder import build_prompt


def generate_response(inp : str, prompt : str):

    response = chat(
        model='mistral:7b',
        messages=[
            {'role' : 'system' , 'content' : prompt},
            {'role' : 'user' , 'content' : inp}]
    )

    return response.message.content

if __name__ == "__main__":
    inp = input("Give your query here : ")
    prompt = build_prompt(inp)
    
    print(generate_response(inp, prompt))
