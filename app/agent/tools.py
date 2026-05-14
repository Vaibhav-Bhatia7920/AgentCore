from app.llm.llm_ops import make_ollama_call

def summarize_file(file_path: str):
    with open(file_path, 'r') as file:
        content = file.read()
    
    summary = make_ollama_call(f"Summarize the following content: {content}", model="mistral:7b")
    return summary
