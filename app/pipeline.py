from app.llm.llm import generate_response
from app.llm.control_layer import llm_grounding_check
from app.llm.llm import log_llm_response
from app.llm.trace import log_tracing

def complete_rag_flow(query : str, number : int = 4):
   
    res = generate_response(query, number)
    check = llm_grounding_check(res)
    if check == False:
        print("I am here")
        res.answer = "I don't have an answer"
    res2 = log_llm_response(res , check)
    log_tracing(res2)
    return res2, res
    



if __name__ == "__main__":
    n = 4
    complete_rag_flow(n)