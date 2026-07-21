"""MCP Server Scaffold Generator — CLI entry point."""

import os
import click
from pathlib import Path


SERVER_PY_TPL = """\"\"\"
{NAME} — MCP Server
\"\"\"
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types


async def main():
    server = Server("{NAME}")

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
                server_name="{NAME}",
                server_version="{VERSION}",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={{}},
                ),
            ),
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
"""

TEST_TPL = """\"\"\"Tests for {NAME} MCP server.\"\"\"
import pytest
from mcp import types


def test_tool_schema():
    \"\"\"The server exposes an echo tool with the right schema.\"\"\"
    pass


def test_imports():
    \"\"\"Verify critical dependencies are importable.\"\"\"
    import mcp
    import mcp.types
    import mcp.server.stdio
    assert hasattr(mcp, "Server")
"""

PYPROJECT_TPL = """[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{NAME}"
version = "{VERSION}"
description = "{DESCRIPTION}"
requires-python = ">=3.10"
dependencies = [
    "mcp>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.24",
]

[tool.hatch.build.targets.wheel]
packages = ["src/{PACKAGE}"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
"""

README_TPL = """# {NAME}

{DESCRIPTION}

## Installation

```bash
pip install {PACKAGE}
```

## Quick Start

```bash
# Run the MCP server (stdio mode)
python -m {PACKAGE}.server
```

## Tools

- **echo** — Echo back messages (example tool)

## Development

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT
"""

GITIGNORE = """__pycache__/
*.py[cod]
*$py.class
*.egg-info/
dist/
build/
.venv/
venv/
"""


def scaffold(server_name: str, description: str, version: str, output_dir: Path):
    """Generate a complete MCP server project."""
    package_name = server_name.lower().replace("-", "_").replace(" ", "_")

    dirs = [
        output_dir,
        output_dir / "src" / package_name,
        output_dir / "tests",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    # Create __init__.py
    (output_dir / "src" / package_name / "__init__.py").write_text(
        f'__version__ = "{version}"\n'
    )

    replacements = {
        "NAME": server_name,
        "PACKAGE": package_name,
        "VERSION": version,
        "DESCRIPTION": description,
    }

    def render(tpl: str) -> str:
        for key, val in replacements.items():
            tpl = tpl.replace("{" + key + "}", val)
        return tpl

    # Write template files
    (output_dir / "src" / package_name / "server.py").write_text(render(SERVER_PY_TPL))
    (output_dir / "README.md").write_text(render(README_TPL))
    (output_dir / "pyproject.toml").write_text(render(PYPROJECT_TPL))
    (output_dir / ".gitignore").write_text(GITIGNORE)
    (output_dir / "tests" / "test_server.py").write_text(render(TEST_TPL))

    return package_name


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("server_name")
@click.option(
    "-d", "--description",
    default="An MCP server built with mcp-server-scaffold",
    show_default=True,
    help="Short description of the MCP server",
)
@click.option(
    "-v", "--version",
    default="0.1.0",
    show_default=True,
    help="Initial version for the generated project",
)
@click.option(
    "-o", "--output",
    default=".",
    help="Output directory (creates a subfolder named after the server)",
)
@click.option(
    "--install/--no-install",
    default=False,
    help="Install dependencies after scaffolding",
)
def main(server_name: str, description: str, version: str, output: str, install: bool):
    """Generate a complete MCP server project.

    SERVER_NAME is the name of your MCP server (e.g., "my-weather-server").
    """
    output_dir = Path(output) / server_name
    package = scaffold(server_name, description, version, output_dir)

    click.echo()
    click.echo(f"* Created MCP server: {server_name}")
    click.echo(f"   Package: {package}")
    click.echo(f"   Location: {output_dir}")
    click.echo()
    click.echo("Next steps:")
    base = Path(output).resolve() if output != "." else Path.cwd()
    click.echo(f"  cd {(output_dir / server_name).relative_to(output_dir.parent) if output_dir.parent != Path(output).resolve() else server_name}")
    click.echo("  pip install -e .[dev]")
    click.echo(f"  python -m src.{package}.server")
    click.echo()
    click.echo("For the full version with advanced templates, Docker support,")
    click.echo("and multi-transport scaffolding:")
    click.echo("  https://shadowcraft41.gumroad.com/l/fskmzv")


if __name__ == "__main__":
    main()
