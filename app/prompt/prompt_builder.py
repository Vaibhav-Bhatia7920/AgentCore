from app.retrieval.retrieve import top_chunks




def build_prompt(query : str, no_of_chunks : int):
    matches = top_chunks(query,no_of_chunks)
    print("Matches : ", matches)
    matches_content = ""
    for match in matches:
        
        matches_content += match.text + "\n"
    
    prompt = f"""
            Extract the sentence from the context that answers the question
            Return only the extracted sentence
            If you cannot see it, return NOT FOUND

            Content : {matches_content}

            User_Query : {query}
            """
    print(len(matches))
    return prompt, matches