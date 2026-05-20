import chromadb
from chromadb import PersistentClient
from pathlib import Path
from app.ingest.embedder import embed_chunks
import numpy as np
import os


path1 = Path("/Users/vaibhav/Documents/DevBase/ml-60/Fork/AgentCore/chroma_db")

is_docker = os.path.exists("/.dockerenv")
if is_docker:
    CHROMA_HOST = os.getenv("CHROMA_HOST", "db")
    CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))

    client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
else:
    client = PersistentClient(path = path1)

collection = client.get_or_create_collection(name="AgentCore_Collection", metadata={"hnsw:space": "cosine"})

def store_embeddings():
    embed_dict = embed_chunks()
    
    for key in embed_dict.keys():
        main_dict = embed_dict[key]
        file_name = main_dict["file_name"]
        collection.delete(where={"file_name": file_name})

    for key in embed_dict.keys():
        main_dict = embed_dict[key]
        embedding = np.array(main_dict["embedding"])

        chunk = main_dict["chunk"]
        # print("Chunk : ", chunk , "File Name : ", main_dict["file_name"])
        file_name = main_dict["file_name"]
        file_id = main_dict["file_id"]

        
        collection.upsert(
            embeddings= [embedding[0]],
            documents= [chunk],
            metadatas=[{
                "file_name" : file_name,
                "file_id" : file_id
            }],
            ids = f"{file_name}_chunk_{key}"
        )

if __name__ == "__main__":
    store_embeddings()