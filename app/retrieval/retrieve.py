from chromadb import PersistentClient
from pathlib import Path
from app.ingest.embedder import generate_embeddings
import regex as re
from app.models.chunk_models import ChunkContent

path = Path("/Users/vaibhav/Documents/DevBase/ml-60/Fork/AgentCore/chroma_db")
client = PersistentClient(path)

collection = client.get_or_create_collection(name="AgentCore_Collection")

def normalize_query(query : str):
    res = query.strip()
    res = re.sub(" +"," ",res)
    comps = res.split(" ")
    final_string = (" ".join(comps))
    return final_string

def top_chunks(query : str, number : int):
    query = normalize_query(query)
    print(query)
    query_embedding = generate_embeddings(query)
    results = collection.query(query_embeddings= query_embedding, n_results=number)
    res_dict = []
    for i in range(len(results['ids'][0])):
        res = {"text" : results['documents'][0][i], "file_name" : results['metadatas'][0][i]['file_name'], "chunk_index" : results['metadatas'][0][i]['file_id'], 'similarity_score' : 1 - results["distances"][0][i]}
        chunk = ChunkContent(**res)
        res_dict.append(chunk)
    
    return res_dict

if __name__ == "__main__":
    inp  = input("Enter your query here : ")
    res_vec = top_chunks(inp)
    for i in range(len(res_vec)):
        print(res_vec[i])
