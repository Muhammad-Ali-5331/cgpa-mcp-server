# PUCIT CGPA Guider — Assignment 3 (BCSF24A022)

LangGraph agent with **memory** (async SQLite checkpointer), **streaming**
(`astream`, `updates` + `messages`) and its tools served from an **MCP server**.

## Submission details

- **MCP server URL:** `https://cgpa-mcp-server-ttrt.onrender.com/mcp`
- **GitHub repo (server code):** `https://github.com/Muhammad-Ali-5331/cgpa-mcp-server`

## Layout

```
server.py (FastMCP, 8 tools)  tools.py  requirements.txt .env.example
agent/    main.py (chat loop)  graph.py (StateGraph)  mcp_adapter.py (MCP client) llm.py system_prompt.py
```

## Run locally

```
# Install Requirements + Setup ENV vars
cp .env.example .env        # add GROQ_API_KEY (+ MCP_URL, FASTMCP_KEY if hosted)
pip install -r requirements.tx

# terminal 1 - server
python server.py     # http://127.0.0.1:8000/mcp

# test the server alone (no LLM, no key)
fastmcp list server.py
fastmcp call server.py get_credit_hours semesters='[5,6]'            # 37.0

# terminal 2 - agent
cd agent
python main.py
```

Commands in the chat: `/switch`, `/history`, `/forget`, `/quit`.

## Hosting (Task 5)

The server binds `0.0.0.0:$PORT` when `PORT` is set (Render/Horizon style).
Render: Web Service -> build `pip install -r requirements.txt` -> start `python server.py`. Then set `MCP_URL=https://<app>.onrender.com/mcp` in `.env` (and `FASTMCP_KEY` if the host requires auth). No agent code changes.

## Task 6 — server down

1. `mcp_adapter.py` catches connection errors and returns a `TOOL_ERROR ...` string,
   so every tool call always gets a `ToolMessage` answer.
2. `ToolNode(handle_tool_errors=True)` converts any other tool exception the same way.
3. `graph.patch_dangling_tool_calls` repairs chats that *already* contain an
   unanswered tool call by inserting a synthetic "this call never ran" `ToolMessage`
   before the messages go to the model.

## Note

`save_report` runs on the server, so reports are written on the *server's* disk.
