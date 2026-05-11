from app.retrieval.retrieve import top_chunks
from app.db.db_ops import get_last_n_messages, get_long_term_memory



def build_prompt(query : str, no_of_chunks : int, session_id : int = None):
    matches = top_chunks(query,no_of_chunks)
    print("Matches : ", matches)
    matches_content = ""
    context_window = get_last_n_messages(session_id, 10)
    cross_session_memory = get_long_term_memory()
    for match in matches:
        
        matches_content += match.text + "\n"
    
    prompt = f"""
            Extract the sentence from the context that answers the question
            Return only the extracted sentence
            If you cannot see it, return NOT FOUND
            
            Context : {context_window}

            Cross Session Memory : {cross_session_memory}
            
            Content : {matches_content}

            User_Query : {query}
            """
    print(len(matches))
    return prompt, matches