# File System MCP Server

A Model Context Protocol (MCP) server that provides tools for interacting with files and directories using Python.

## Features

This MCP server provides the following tools:

- **read_file** - Read the contents of a file
- **write_file** - Write content to a file (creates file if it doesn't exist)
- **list_directory** - List the contents of a directory
- **create_directory** - Create a directory (with optional parent directory creation)
- **delete_file** - Delete a file or directory (with optional recursive deletion)
- **move_file** - Move or rename a file or directory
- **copy_file** - Copy a file or directory to a new location
- **file_exists** - Check if a file or directory exists
- **get_file_info** - Get detailed information about a file or directory

## Installation

1. Install Python 3.8 or higher

2. Install the required dependencies:

The MCP Python SDK can be installed from GitHub:
```bash
pip install git+https://github.com/modelcontextprotocol/python-sdk.git
```

Or if available on PyPI:
```bash
pip install mcp
```

Alternatively, install from requirements.txt:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Server

The server uses stdio (standard input/output) for communication:

```bash
python server.py
```

### Configuration

To use this MCP server with an MCP client (like Cursor), add it to your MCP configuration file.

For Cursor, add to your MCP settings (typically in `~/.cursor/mcp.json` or similar):

```json
{
  "mcpServers": {
    "file-system": {
      "command": "python",
      "args": ["/path/to/file-system-mcp-server/server.py"]
    }
  }
}
```

Or if you've installed it in a virtual environment:

```json
{
  "mcpServers": {
    "file-system": {
      "command": "/path/to/venv/bin/python",
      "args": ["/path/to/file-system-mcp-server/server.py"]
    }
  }
}
```

### Example Tool Usage

Once connected, you can use the tools through your MCP client:

- **Read a file**: `read_file` with `{"path": "/path/to/file.txt"}`
- **Write a file**: `write_file` with `{"path": "/path/to/file.txt", "content": "Hello, World!"}`
- **List directory**: `list_directory` with `{"path": "/path/to/directory"}`
- **Create directory**: `create_directory` with `{"path": "/path/to/newdir", "parents": true}`
- **Delete file**: `delete_file` with `{"path": "/path/to/file.txt"}`
- **Move file**: `move_file` with `{"source": "/old/path", "destination": "/new/path"}`
- **Copy file**: `copy_file` with `{"source": "/source/path", "destination": "/dest/path"}`
- **Check existence**: `file_exists` with `{"path": "/path/to/check"}`
- **Get file info**: `get_file_info` with `{"path": "/path/to/file"}`

## MCP Client with Gemini Flash

The project includes `mcp_client.py`, a client that uses Google's Gemini Flash LLM model to intelligently process natural language requests and communicate with the MCP server.

### Client Setup

1. Install additional dependencies:
```bash
pip install google-generativeai
```

2. Set your Gemini API key:
```bash
export GEMINI_API_KEY=your_api_key_here
```

Or get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

### Using the Client

#### Interactive Mode

Run the client in interactive mode to process natural language requests:

```bash
python mcp_client.py
```

Example interactions:
```
> Read the file README.md
> List all files in the current directory
> Create a directory called test_folder
> Write "Hello World" to hello.txt
> Check if server.py exists
```

#### Single Request Mode

Process a single request non-interactively:

```bash
python mcp_client.py --request "List files in the current directory"
```

#### Command Line Options

```bash
python mcp_client.py --help

Options:
  --server PATH     Path to MCP server script (default: server.py)
  --api-key KEY    Google Gemini API key (or set GEMINI_API_KEY env var)
  --model MODEL    Gemini model to use (default: gemini-1.5-flash)
  --request TEXT   Single request to process (non-interactive mode)
```

### How It Works

1. The client connects to the MCP server via stdio
2. It uses Gemini Flash LLM to understand natural language requests
3. Gemini determines which MCP tools to use based on available tools
4. The client executes the tool calls on the MCP server
5. Results are returned and displayed

### Example Usage

```python
import asyncio
from mcp_client import MCPFileSystemClient

async def main():
    client = MCPFileSystemClient(
        server_script="server.py",
        gemini_api_key="your-api-key",  # or set GEMINI_API_KEY env var
        model="gemini-1.5-flash"
    )
    
    await client.connect()
    
    # Process a natural language request
    result = await client.process_request("Read the file README.md")
    print(result)
    
    await client.disconnect()

asyncio.run(main())
```

## Security Note

⚠️ **Important**: This server provides full file system access. Be cautious when configuring it and ensure you trust the MCP client that will be using it. Consider restricting access to specific directories if needed.

## License

This project is provided as-is for use with the Model Context Protocol.

