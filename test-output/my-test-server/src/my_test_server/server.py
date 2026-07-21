"""
my-test-server — MCP Server
"""
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types


async def main():
    server = Server("my-test-server")

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name="echo",
                description="Echo back the input message",
                input_schema={{"type": "object", "properties": {{"message": {{"type": "string", "description": "Message to echo"}}}}, "required": ["message"]}},
            ),
        ]

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        if name == "echo":
            return [types.TextContent(type="text", text=f"Echo: {{arguments['message']}}")]
        raise ValueError(f"Unknown tool: {{name}}")

    @server.list_resources()
    async def handle_list_resources() -> list[types.Resource]:
        return []

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="my-test-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={{}},
                ),
            ),
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
