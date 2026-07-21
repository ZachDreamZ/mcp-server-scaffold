# MCP Server Scaffold Generator

Generate a production-ready MCP (Model Context Protocol) server project from a single command.

```bash
pip install mcp-server-scaffold
mcp-scaffold my-weather-server --description "Weather data MCP server"
cd my-weather-server
pip install -e ".[dev]"
python -m src.my_weather_server.server
```

## Features

| Feature | Free | Paid ($9) |
|---------|:----:|:---------:|
| Basic MCP server scaffold | ✅ | ✅ |
| Echo tool example | ✅ | ✅ |
| Pyproject and project structure | ✅ | ✅ |
| Pytest setup | ✅ | ✅ |
| Advanced templates (HTTP/SSE transport) | ❌ | ✅ |
| Dockerfile and compose | ❌ | ✅ |
| Pre-built tool examples (search, fetch, DB) | ❌ | ✅ |
| FastAPI + MCP hybrid template | ❌ | ✅ |
| Resource subscription examples | ❌ | ✅ |
| Cursor/Claude Desktop config snippets | ❌ | ✅ |

## Why?

Setting up an MCP server from scratch requires:
- Installing "mcp" and understanding its async API
- Wiring up stdio transport correctly
- Creating the right project structure
- Writing tool/resource handlers

This scaffold does it all in one command.

## Paid Version

Get the full version with advanced templates at shadowcraft41.gumroad.com/l/fskmzv

Use code LAUNCH for 50% off.

## GitHub

github.com/ZachDreamZ/mcp-server-scaffold
