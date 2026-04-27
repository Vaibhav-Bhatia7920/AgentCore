from app.ingest.chunker import chunk_content
import ollama
import numpy as np

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

    for key in chunk_dict.keys():
        embedding = generate_embeddings(chunk_dict[key]["chunk"])
        embed_dict[key] = {"file_name" : chunk_dict[key]["file_name"], "file_id" : chunk_dict[key]["file_id"], "chunk" : chunk_dict[key]["chunk"], "embedding" : embedding}
    
    return embed_dict
        