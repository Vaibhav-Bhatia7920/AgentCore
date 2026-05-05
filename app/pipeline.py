from app.llm.llm import generate_response
from app.llm.control_layer import llm_grounding_check
from app.llm.llm import log_llm_response
from app.llm.llm import log_llm_response2
from app.llm.trace import log_tracing
from app.llm.mock_llm import mock_generate_response
import json
from pathlib import Path

def complete_rag_flow(query : str, number : int = 4):
   
    res = generate_response(query, number)
    check = llm_grounding_check(res)
    if check == False:
        print("I am here")
        res.answer = "I don't have an answer"
    res2 = log_llm_response(res , check)
    log_tracing(res2)
    return res2, res
    
def complete_rag_flow_mock(query : str, number : int = 4):

    res = mock_generate_response(query, number)
    check = llm_grounding_check(res)
    if check == False:
        print("I am here")
        res.answer = "I don't have an answer"
    res2 = log_llm_response(res , check)
    log_tracing(res2)
    return res2, res

def complete_rag_flow_golden_dataset(query : str, number : int = 4):

    res = generate_response(query, number)
    check = llm_grounding_check(res)
    if check == False:
        print("I am here")
        res.answer = "I don't have an answer"
    res2 = log_llm_response2(res , check)
    return res2, res

if __name__ == "__main__":
    n = 4
    file = Path(__file__).resolve().parent.parent / "tests" / "golden_test.jsonl"
    # with open(file, 'r') as f:
    #     data = json.load(f)
    #     for item in data:
    #         inp = item['question']
    #         _ , _ = complete_rag_flow_golden_dataset(inp, n)
    inp = input("Enter your query here : ")
    res, _ = complete_rag_flow(inp, n)
    
    