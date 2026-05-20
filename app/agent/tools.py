import os
from chromadb import PersistentClient
from app.llm.llm_ops import make_ollama_call
from ollama import chat
from app.models.agent_models import AgentTrace, AgentStep, ToolCall
from app.agent.trace_logger import log_agent_trace
from app.retrieval.retrieve import top_chunks_for_agent_file, top_chunks_for_agent_global
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
agent_logic_model = os.getenv("agent_logic_model")
summary_model = os.getenv("rag_response_model")

path = Path("/Users/vaibhav/Documents/DevBase/ml-60/Fork/AgentCore/chroma_db")
client = PersistentClient(path)
collection = client.get_or_create_collection(name="AgentCore_Collection")


def get_top_chunks_file(query: str, file_name: str, top_k: int = 3):
    """
    Retrieve the top K most relevant chunks for a specific file from the ChromaDB collection."""
    return top_chunks_for_agent_file(query=query, file_name=file_name, number=top_k)

def get_top_chunks_global(query: str, top_k: int = 3):
    """
    Retrieve the top K most relevant chunks from the entire ChromaDB collection."""
    return top_chunks_for_agent_global(query=query, number=top_k)

def list_files_in_directory(directory_path: str):
    return os.listdir(directory_path)

def get_the_temperature_of_a_city(city_name: str):
    return f"The current temperature in {city_name} is 25 degrees Celsius."

def edit_file(file_path: str, new_content: str):
    with open(file_path, 'w') as file:
        file.write(new_content)
    return f"File at {file_path} has been updated."

# def group_files_by_topics(directory_path: str):
#     files = os.listdir(directory_path)
#     topic_groups = {}
    

def add(n1 : int, n2 : int):
    return n1 + n2

def multiply(n1 : int, n2 : int):
    return n1 * n2

def divide(n1 : int, n2 : int):
    if n2 == 0:
        return "Cannot divide by zero."
    return n1 / n2

availaible_tools = {
    "list_files_in_directory" : list_files_in_directory,
    "get_the_temperature_of_a_city" : get_the_temperature_of_a_city,
    "get_top_chunks_file" : get_top_chunks_file,
    "get_top_chunks_global" : get_top_chunks_global,
    "edit_file" : edit_file,
    "add" : add,
    "multiply" : multiply,
    "divide" : divide
}

# def ollama_tool_call(tool_list : list , query : str):
#     messages = [{"role" : "user", "content" : query}]
#     response = chat(model=agent_logic_model, messages=messages, tools=tool_list, think=True)

#     messages.append(response.message)
#     if response.message.tool_calls:
#         call = response.message.tool_calls[0]
#         result = summarize_file(**call.function.arguments)

#         messages.append({"role" : "tool", "tool_name" : call.function.name, "content" : str(result)})

#         final_response = chat(model=agent_logic_model, messages=messages, tools=tool_list, think=True)
#         print(final_response.message.content)


def ollama_tool_call_parallel(tool_list : list , query : str):
    messages = [{"role" : "user", "content" : query}]
    agent_trace = AgentTrace(query = query, steps = [], response = "")

    while True: 
        response = chat(model=agent_logic_model, messages=messages, tools=tool_list, think=True)
        messages.append(response.message)
        print(response.message)
        if response.message.tool_calls:
            print(response.message.tool_calls)
            for call in response.message.tool_calls:
                tool_call = ToolCall(tool_name = call.function.name, arguments = call.function.arguments)
                if call.function.name in availaible_tools:
                    print(f"Calling tool: {call.function.name}")
                    result = availaible_tools[call.function.name](**call.function.arguments)
                    print(f"Result from tool: {result}")
                    messages.append({"role" : "tool", "tool_name" : call.function.name, "content" : str(result)})
                    agent_step = AgentStep(thought = response.message.thinking, tool_calls = [tool_call], observation = str(result))
                    agent_trace.steps.append(agent_step)
        else:
            print("In breaking loop")
            break
    print("here")
    agent_trace.response = response.message.content
    print(response.message.content)
    return agent_trace

if __name__ == "__main__":
    tool_list = [list_files_in_directory, get_the_temperature_of_a_city, edit_file, add, multiply, divide, get_top_chunks_file, get_top_chunks_global]
    query = input("Enter your query: ")
    agent_trace = ollama_tool_call_parallel(tool_list, query)
    log_agent_trace(agent_trace)
