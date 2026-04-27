from app.ingest.loader import load_files
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_content():
    chunk_dict = {}
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 100,
        chunk_overlap = 10
    )
    file_dict = load_files()
    ind = 0
    for key in file_dict.keys():
        chunks = text_splitter.split_text(file_dict[key]["content"])
        for chunk in chunks:
            chunk_dict[ind] = {"file_name" : file_dict[key]["file"], "file_id" : key, "chunk" : chunk}
            ind += 1

    return chunk_dict
