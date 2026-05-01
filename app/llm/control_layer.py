import yake
from rake_nltk import Rake
from app.models.llm_models import RAGResponse


def grouding_check(llm_response : RAGResponse):
    kw_extractor = yake.KeywordExtractor()
    chunks = llm_response.chunk_retrieved
    chunk_text = ""
    for chunk in chunks:
        chunk_text += chunk.text
        chunk_text += "\n"
    
    answer = llm_response.answer
    
    keywords = kw_extractor.extract_keywords(answer)
    for phrase,_ in keywords:
        phrase = phrase.split(" ")

    keywords1 = []
    for phrase,_ in keywords:
        for words in phrase:
            keywords1.append(words)
    
    score = 0
    
    total_size = len(keywords1)
    present = 0
    for words in keywords1:
        if words in chunk_text:
            present += 1
    
    score = present / total_size
    
    if score > 0.85:
        return True
    else:
        return False

