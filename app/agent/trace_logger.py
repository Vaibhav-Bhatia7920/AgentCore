from app.models.agent_models import AgentTrace, AgentStep, ToolCall

def log_agent_trace(agent_trace: AgentTrace):
    print("Logging Agent Trace:")
    print(f"Query: {agent_trace.query}")
    print(len(agent_trace.steps))
    for i, step in enumerate(agent_trace.steps):
        print(f"Step {i+1}:")
        print(f"  Thought: {step.thought}")
        for tool_call in step.tool_calls:
            print(f"  Tool Call: {tool_call.tool_name} with arguments {tool_call.arguments}")
        print(f"  Observation: {step.observation}")
    print(f"Final Response: {agent_trace.response}")