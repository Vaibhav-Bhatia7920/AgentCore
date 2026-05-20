import chromadb
import ollama
import os   
from chromadb import PersistentClient
from pathlib import Path
from app.ingest.embedder import generate_embeddings
import regex as re
from app.models.chunk_models import ChunkContent
from app.ingest.embedder import cosine_similarity, file_level_embeddings
import numpy as np
from app.llm.control_layer import grouding_check

path1 = Path("/Users/vaibhav/Documents/DevBase/ml-60/Fork/AgentCore/chroma_db")

is_docker = os.path.exists("/.dockerenv")
if is_docker:
    CHROMA_HOST = os.getenv("CHROMA_HOST", "db")
    CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))

    client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
else:
    client = PersistentClient(path = path1)

collection = client.get_or_create_collection(name="AgentCore_Collection", metadata={"hnsw:space": "cosine"})

def normalize_query(query : str):
    res = query.strip()
    res = re.sub(" +"," ",res)
    comps = res.split(" ")
    final_string = (" ".join(comps))
    return final_string

def preoptimize_query(query : str):
    query = normalize_query(query)
    query_embedding = generate_embeddings(query)

    return query_embedding

def top_chunks_for_agent_file(query : str, file_name : str, number : int):
    query_embedding = preoptimize_query(query)
    file_name = file_name
    results = collection.query(query_embeddings= query_embedding, n_results=number, where={"file_name" : file_name})
    return results['documents'][0]

def top_chunks_for_agent_global(query : str, number : int):
    return top_chunks_with_reranking(query, number)

def top_chunks(query : str, number : int):
    query = normalize_query(query)
    query_embedding = generate_embeddings(query)
    file_name = ""
    score = 0
    file_embeddings, file_summary = file_level_embeddings()
    for key,embedding in file_embeddings.items():
        score_1 = cosine_similarity(np.squeeze(query_embedding), np.squeeze(embedding))
        score_2 = grouding_check(query, file_summary[key])
        final_score = 0.75 * score_2 + 0.25 * score_1
        if final_score > score:
            score = final_score
            file_name = key
    
   
    
   
    results = collection.query(query_embeddings= query_embedding, n_results=number, where={"file_name" : file_name})
    res_dict = []
   

    for i in range(len(results['ids'][0])):
      
        res = {"text" : results['documents'][0][i], "file_name" : results['metadatas'][0][i]['file_name'], "chunk_index" : results['metadatas'][0][i]['file_id'], 'similarity_score' : 1 - results["distances"][0][i]}
        chunk = ChunkContent(**res)
        res_dict.append(chunk)
   
    return res_dict

def top_chunks_with_reranking(query: str, number: int):
    chunks = top_chunks(query, number * 3)
    scored_chunks = []

    for chunk in chunks:
        prompt = (
            f"System: Rate the relevance of the document to the query on a scale from 0 to 10.\n"
            f"Query: {query}\n"
            f"Document: {chunk.text}\n"
            f"Relevance Score (0-10):"
        )
        
        try:
            response = ollama.generate(
                model="dengcao/Qwen3-Reranker-4B:Q5_K_M",
                prompt=prompt,
                options={
                    "temperature": 0.0,       
                    "num_predict": 3,         
                    "stop": ["\n"]           
                }
            )
            
            cleaned_response = response['response'].strip()
            print(f"Chunk text snippet: {chunk.text[:30]}... -> Model Response: {cleaned_response}")
            
            score = float(''.join(c for c in cleaned_response if c.isdigit() or c == '.'))
            scored_chunks.append((score, chunk))
            
        except Exception as e:
            print(f"Skipping a glitched chunk: {e}")
            scored_chunks.append((0.0, chunk))

    scored_chunks.sort(key=lambda x: x[0], reverse=True)

    top_results = [chunk for score, chunk in scored_chunks[:number]]
    return top_results

if __name__ == "__main__":
    inp = input("Enter your query here: ")
    res_vec = top_chunks_with_reranking(inp, 3)
    for res in res_vec:
        print(f"File: {res.file_name}, Chunk Index: {res.chunk_index}, Similarity Score: {res.similarity_score}")
        print(f"Text: {res.text}\n")
    
