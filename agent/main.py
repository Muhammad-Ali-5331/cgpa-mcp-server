"""
CGPA Guider - console chat with MEMORY (SQLite), STREAMING and MCP tools.
Run the server first (cd server && python server.py), then:  python main.py
"""
import asyncio
import os

from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from mcp_adapter import MCPAdapter
from graph import build_app

MCP_URL = os.getenv("MCP_URL", "http://127.0.0.1:8000/mcp")
KEY = os.getenv("FASTMCP_KEY") or None          # None -> no auth (local server)
DB_FILE = "chats.db"


async def list_threads(memory) -> list[str]:
    """Every thread_id that has at least one checkpoint in the SQLite file."""
    seen = []
    async for ckpt in memory.alist(None):
        tid = ckpt.config["configurable"]["thread_id"]
        if tid not in seen:
            seen.append(tid)
    return seen


async def show_history(app, config) -> None:
    state = await app.aget_state(config)
    messages = state.values.get("messages", [])
    if not messages:
        print("  (no saved messages)")
        return
    for m in messages:
        if isinstance(m, HumanMessage):
            print(f"  You  : {m.content}")
        elif isinstance(m, AIMessage):
            for call in m.tool_calls:
                print(f"  [tool call] {call['name']}({call['args']})")
            if m.content:
                print(f"  Agent: {m.content}")
        elif isinstance(m, ToolMessage):
            print(f"  [tool result] {m.content}")


async def stream_reply(app, text: str, config) -> None:
    inputs = {"messages": [HumanMessage(text)]}
    printing_answer = False

    async for chunk in app.astream(inputs, config, stream_mode=["updates", "messages"], version="v2"):
        if chunk["type"] == "messages":
            token, metadata = chunk["data"]
            if metadata["langgraph_node"] == "agent" and token.content:
                if not printing_answer:
                    print("Agent: ", end="", flush=True)
                    printing_answer = True
                print(token.content, end="", flush=True)
        else:
            for node, update in chunk["data"].items():
                for m in update.get("messages", []):
                    if node == "agent" and m.tool_calls:
                        if printing_answer:
                            print()
                            printing_answer = False
                        for call in m.tool_calls:
                            print(f"  >> calling {call['name']}({call['args']}) ...", flush=True)
                    elif node == "tools":
                        print(f"  << {m.name} returned: {m.content}", flush=True)
    if printing_answer:
        print()


async def choose_person(memory) -> str:
    saved = await list_threads(memory)
    print("Saved chats:", ", ".join(saved) if saved else "(none yet)")
    while True:
        name = input("Who is chatting? (your name) > ").strip()
        if name:
            return name


async def main():
    try:
        tools = await MCPAdapter(MCP_URL, auth=KEY).list_tools()
    except Exception as exc:
        print(f"Cannot reach the MCP server at {MCP_URL}: {type(exc).__name__}: {exc}")
        print("Start it with: cd server && python server.py")
        return
    print(f"Connected to {MCP_URL} - {len(tools)} tools: {', '.join(t.name for t in tools)}")

    from llm import LLM

    async with AsyncSqliteSaver.from_conn_string(DB_FILE) as memory:
        app = build_app(LLM, tools, memory)

        name = await choose_person(memory)
        config = {"configurable": {"thread_id": name}}
        print(f"Hi {name}! Commands: /switch  /history  /forget  /quit")

        while True:
            text = input(f"\n[{name}] You > ").strip()
            if not text:
                continue
            if text == "/quit":
                break
            if text == "/switch":
                name = await choose_person(memory)
                config = {"configurable": {"thread_id": name}}
                print(f"Switched to {name}.")
                continue
            if text == "/history":
                await show_history(app, config)
                continue
            if text == "/forget":
                await memory.adelete_thread(name)
                print(f"Deleted everything saved for {name}.")
                continue

            try:
                await stream_reply(app, text, config)
            except Exception as exc:
                print(f"\n[error] {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    asyncio.run(main())
