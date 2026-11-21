from langchain_core.messages import AIMessage, SystemMessage, ToolMessage
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition

from system_prompt import SYSTEM_PROMPT,SERVER_DOWN_NOTE

def patch_dangling_tool_calls(messages: list) -> list:
    fixed = []
    for i, msg in enumerate(messages):
        fixed.append(msg)
        if isinstance(msg, AIMessage) and msg.tool_calls:
            answered = {m.tool_call_id for m in messages[i + 1:] if isinstance(m, ToolMessage)}
            for call in msg.tool_calls:
                if call["id"] not in answered:
                    fixed.append(ToolMessage(content=SERVER_DOWN_NOTE, tool_call_id=call["id"], name=call["name"]))
    return fixed


def build_app(llm, tools, checkpointer):
    llm_with_tools = llm.bind_tools(tools)

    async def agent_node(state: MessagesState):
        history = patch_dangling_tool_calls(state["messages"])
        reply = await llm_with_tools.ainvoke([SystemMessage(SYSTEM_PROMPT)] + history)
        return {"messages": [reply]}
    
    tool_node = ToolNode(tools, handle_tool_errors=True)

    builder = StateGraph(MessagesState)
    builder.add_node("agent", agent_node)
    builder.add_node("tools", tool_node)
    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", tools_condition)
    builder.add_edge("tools", "agent")
    return builder.compile(checkpointer=checkpointer)