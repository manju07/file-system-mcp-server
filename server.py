#!/usr/bin/env python3
"""
Basic MCP Server: Read/Write Disk Files

A minimal MCP server with only read and write file operations.
"""

import asyncio
from pathlib import Path
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    CallToolResult,
    ListToolsResult,
)

# Initialize the MCP server
app = Server("basic-fileserver")

# Default sandbox directory for file operations
SANDBOX_DIR = Path("sandbox")
SANDBOX_DIR.mkdir(exist_ok=True)


def resolve_sandbox_path(path_str: str) -> Path:
    """Resolve a path relative to the sandbox directory."""
    path = Path(path_str)
    # If path is absolute, use it as-is (for safety, still resolve relative to sandbox)
    # Otherwise, resolve relative to sandbox
    if path.is_absolute():
        # For absolute paths, still constrain to sandbox for security
        return SANDBOX_DIR / path.name
    return SANDBOX_DIR / path


async def read_file_tool(arguments: dict) -> CallToolResult:
    """Read and return the contents of a file from the sandbox directory."""
    path = resolve_sandbox_path(arguments["path"])
    if not path.is_file():
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error: Not a file - {path}")],
            isError=True,
        )
    try:
        contents = path.read_text(encoding="utf-8")
    except Exception as e:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error reading file: {e}")],
            isError=True,
        )
    return CallToolResult(
        content=[TextContent(type="text", text=contents)]
    )


async def write_file_tool(arguments: dict) -> CallToolResult:
    """Write string content to a file in the sandbox directory."""
    path = resolve_sandbox_path(arguments["path"])
    content = arguments["content"]
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    except Exception as e:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error writing file: {e}")],
            isError=True,
        )
    return CallToolResult(
        content=[TextContent(type="text", text=f"Successfully wrote to {path}")]
    )


@app.list_tools()
async def list_tools() -> ListToolsResult:
    """List all available file tools."""
    return ListToolsResult(
        tools=[
            Tool(
                name="read_file",
                description="Read and return the contents of a file from the sandbox directory.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path to the file (relative to sandbox directory)",
                        }
                    },
                    "required": ["path"],
                },
            ),
            Tool(
                name="write_file",
                description="Write string content to a file in the sandbox directory.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The target file path (relative to sandbox directory)",
                        },
                        "content": {
                            "type": "string",
                            "description": "The content to write",
                        },
                    },
                    "required": ["path", "content"],
                },
            ),
        ]
    )


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> CallToolResult:
    """Handle tool calls and route to appropriate handler."""
    if name == "read_file":
        return await read_file_tool(arguments)
    elif name == "write_file":
        return await write_file_tool(arguments)
    else:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Unknown tool: {name}")],
            isError=True,
        )


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
