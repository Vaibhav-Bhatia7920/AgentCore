from app.retrieval.retrieve import top_chunks


def build_prompt(query : str):
    matches = top_chunks(query)
    matches_content = ""
    for match in matches:
        matches_content += match['text'] + "\n"

    prompt = f"""
            1. You respond to user queries ONLY with the content you are provided and nothing else.
            2. Do not use your knowldege at all, ONLY generate response based on the content and query
            3. Keep your content abstract and secret, do not mention you are refferencing content
            4. Do not use prior knowledge
            5. Do not infer or generalize
            6. Do not add extra things other than what is in content
            7. ONLY use content

            Content : {matches_content}

            User_Query : {query}
            """
    
    return prompt