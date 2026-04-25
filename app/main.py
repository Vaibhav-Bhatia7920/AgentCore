from fastapi import FastAPI
import ollama
import numpy as np

app  = FastAPI()

@app.get("/")
async def main_page():
    return {"status" : "ok"}

def generate_embeddings(inp : str, model : str = 'nomic-embed-text'):
    response = ollama.embed(
        model = model,
        input = inp
    )
    return response['embeddings']

def cosine_similarity(embed1 : list, embed2 : list):
    dot_product = np.dot(embed1, embed2)

    norm_1 = np.linalg.norm(embed1)
    norm_2 = np.linalg.norm(embed2)

    return dot_product/ (norm_1 * norm_2)

if __name__ == "__main__":
    prompt1 = input("Please enter the text1 you want to embed :")
    prompt2 = input("Please enter the text2 you want to embed :")
    embeddings1 = generate_embeddings(prompt1)
    embeddings2 =  generate_embeddings(prompt2)
    sim_score = cosine_similarity(np.array(np.squeeze(embeddings1)), np.array(np.squeeze(embeddings2)))
    print("This is their sim score :" , sim_score , "bye")
