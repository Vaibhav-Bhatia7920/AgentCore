from app.models.logs_model import Logs

def log_tracing(inp : Logs):
    print("--RAGResponse(IO)--")
    print(f"Input: {inp.query}")
    print(f"Output: {inp.answer}")

    print("--Chunks Retrieved--")
    for chunk in inp.chunks_dict:
        print(f"Chunk Retrieved: {chunk.text}")
        print(f"Similarity Score: {chunk.similarity_score}")
    
    print(f"Model Used: {inp.model}")

    print(f"Grounding Check: {inp.grounding_check}")

    