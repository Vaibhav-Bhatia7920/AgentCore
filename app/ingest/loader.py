import os
from pathlib import Path
## Also can use the sort of relative path using Path library and getting current file path using __file__,
## then .parent to go to the desired directory

is_docker = os.path.exists("/.dockerenv")
if is_docker:
    directory = Path("/app/data")
else:
    directory = Path("/Users/vaibhav/Documents/DevBase/ml-60/Fork/AgentCore/data")
def load_files():
    file_contents = {}
    ind = 0
    for file_path in directory.iterdir():
        print(file_path)
        if file_path.is_file():
            ind += 1
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                file_contents[ind] = {"file" : file_path.name , "content" : content}
    
    return file_contents

if __name__ == "__main__":
    load_files()