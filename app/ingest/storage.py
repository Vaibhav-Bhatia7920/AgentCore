import chromadb
from chromadb import PersistentClient
from pwdlib import Path
from app.ingest.embedder import generate_embeddings

path1 = Path("/Users/vaibhav/Documents/DevBase/ml-60/Fork/AgentCore/chroma_db")

client = PersistentClient(path = path1)
collection = client.get_or_create_collection(name="AgentCore_Collection")

def store_embeddings():
    embed_dict = generate_embeddings()
    
    for key in embed_dict.keys:
        main_dict = embed_dict[key]
        embedding = main_dict["embedding"]
        chunk = main_dict["chunk"]
        file_name = main_dict["file_name"]
        file_id = main_dict["file_id"]
        collection.add(
            embeddings= [embedding],
            documents= [chunk],
            metadatas=[{
                "file_name" : file_name,
                "file_id" : file_id
            }],
            id = [key]
        )