from fastmcp.client import Client
from langchain_core.tools import StructuredTool


class MCPAdapter:
    def __init__(self, target, auth=None, timeout: float = 15):
        self.target = target
        self.auth = auth
        self.timeout = timeout
    
    
    def _new_client(self) -> Client:
        if isinstance(self.target, Client):
            return self.target
        return Client(self.target, auth=self.auth, timeout=self.timeout)

    
    async def list_tools(self) -> list[StructuredTool]:
        """connect -> tools/list -> disconnect, return LangChain tools."""
        async with self._new_client() as client:
            mcp_tools = await client.list_tools()
        return [self._to_langchain(t) for t in mcp_tools]


    async def __aenter__(self):
        return self

    
    async def __aexit__(self, *exc):
        return False

    
    def _to_langchain(self, mcp_tool) -> StructuredTool:
        name = mcp_tool.name

        async def _call(**kwargs):
            try:
                async with self._new_client() as client:
                    result = await client.call_tool(name, kwargs, raise_on_error=False)
            except Exception as exc:
                return (f"TOOL_ERROR: the tool server is unreachable right now "
                        f"({type(exc).__name__}). The tool '{name}' did NOT run. "
                        f"Tell the user the calculation service is down and to try again later; "
                        f"do not guess the answer.")
            text = "\n".join(getattr(c, "text", "") for c in result.content).strip()
            if result.is_error:
                return f"TOOL_ERROR: {text or 'the tool failed'}"
            return text

        return StructuredTool(
            name=name,
            description=mcp_tool.description or name,
            args_schema=getattr(mcp_tool, "input_schema", None) or mcp_tool.inputSchema,
            coroutine=_call,
        )
