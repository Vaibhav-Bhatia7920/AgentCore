import json
from urllib import response

from app.ingest.chunker import chunk_content
import ollama
import numpy as np
from pathlib import Path
from ollama import chat

file_embeddings = {}


def generate_response(inp : str):
    response = chat(
        model='mistral:7b',
        messages=[
            {'role' : 'user' , 'content' : inp}]
    )
    subsequent_response = response.message.content
    return subsequent_response
    
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

def embed_chunks():
    chunk_dict = chunk_content()
    embed_dict = {}
    file_embeddings = {}
    file_summary = {}
    content = ""
    for key in chunk_dict.keys():
        embedding = generate_embeddings(chunk_dict[key]["chunk"])
        embed_dict[key] = {"file_name" : chunk_dict[key]["file_name"], "file_id" : chunk_dict[key]["file_id"], "chunk" : chunk_dict[key]["chunk"], "embedding" : embedding}
        
        
        if chunk_dict[key]["file_name"] not in file_embeddings:
            base_dir = Path(__file__).resolve().parent.parent.parent
            file_path = base_dir / "data" / chunk_dict[key]["file_name"]

            with open(file_path, 'r') as f:
                content = f.read()
            content_summary = generate_response("Summarize the following content in  STRICTLY less than 10 words " + content)
            print(content_summary)
            file_embedding = generate_embeddings(content_summary)
            print("Embedding file")
            file_summary[chunk_dict[key]["file_name"]] = content_summary
            file_embeddings[chunk_dict[key]["file_name"]] = [file_embedding[0]]
            
        
    base_dir = Path(__file__).resolve().parent.parent
    file_path1 = base_dir / "logger" / "file_embeddings.json"
    file_path2 = base_dir / "logger" / "file_summary.json"

    with open(file_path1,'w') as file:
        json.dump(file_embeddings, file, indent = 4)        
    
    with open(file_path2,'w') as file:
        json.dump(file_summary, file, indent = 4)

    return embed_dict

def file_level_embeddings():
    base_dir = Path(__file__).resolve().parent.parent
    file_path1 = base_dir / "logger" / "file_embeddings.json"
    file_path2 = base_dir / "logger" / "file_summary.json"

    with open(file_path1,'r') as file:
        file_embeddings = json.load(file)
    with open(file_path2,'r') as file:
        file_summary = json.load(file)
    return file_embeddings, file_summary