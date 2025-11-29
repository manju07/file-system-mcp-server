# File System MCP Server

A minimal Model Context Protocol (MCP) server that provides secure file read and write operations within a sandbox directory. This server is designed to work with MCP clients and includes a Gradio web interface for interactive use.

## Features

This MCP server provides two simple tools:

- **read_file** - Read the contents of a file from the sandbox directory
- **write_file** - Write content to a file in the sandbox directory (creates file if it doesn't exist)

### Security Features

- **Sandbox Directory**: All file operations are restricted to the `sandbox/` directory
- **Path Resolution**: Paths are automatically resolved relative to the sandbox, preventing access to files outside the sandbox
- **Automatic Directory Creation**: Parent directories are automatically created when writing files

## Installation

1. Install Python 3.8 or higher

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

The main dependencies are:
- `openai-agents` - OpenAI Agents SDK (includes MCP support)
- `openai` - OpenAI SDK (used for Gemini API compatibility)
- `gradio` - Web interface framework
- `python-dotenv` - Environment variable management

3. Install the MCP Python SDK:

```bash
pip install git+https://github.com/modelcontextprotocol/python-sdk.git
```

Or if available on PyPI:
```bash
pip install mcp
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

### MCP Client Configuration

To use this MCP server with an MCP client (like Cursor), add it to your MCP configuration file.

For Cursor, add to your MCP settings (typically in `~/.cursor/mcp.json` or similar):

```json
{
  "mcpServers": {
    "file-system": {
      "command": "python3",
      "args": ["/absolute/path/to/file-system-mcp-server/server.py"],
      "env": {}
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
      "args": ["/absolute/path/to/file-system-mcp-server/server.py"],
      "env": {}
    }
  }
}
```

See `example_config.json` for a reference configuration.

## Usage

### Running the MCP Server

The server uses stdio (standard input/output) for communication:

```bash
python server.py
```

### Using the Gradio Web Interface

The project includes a Gradio web interface (`app.py`) that provides an interactive way to use the MCP server with Google's Gemini model:

```bash
python app.py
```

This will:
1. Launch a web interface (typically at `http://127.0.0.1:7860`)
2. Connect to the MCP server
3. Use Gemini 2.0 Flash model to process natural language prompts
4. Execute file operations within the sandbox directory

The interface allows you to enter prompts like:
- "Write a story about a robot"
- "Read the file test.md"
- "Create a file called notes.txt with some content"

### Example Tool Usage

Once connected via an MCP client, you can use the tools:

**Read a file:**
```json
{
  "name": "read_file",
  "arguments": {
    "path": "test.md"
  }
}
```

**Write a file:**
```json
{
  "name": "write_file",
  "arguments": {
    "path": "hello.txt",
    "content": "Hello, World!"
  }
}
```

Note: All paths are relative to the `sandbox/` directory. The server automatically creates the sandbox directory if it doesn't exist.

## Project Structure

```
file-system-mcp-server/
├── server.py              # MCP server implementation
├── app.py                 # Gradio web interface
├── requirements.txt       # Python dependencies
├── example_config.json    # Example MCP client configuration
├── README.md             # This file
└── sandbox/              # Sandbox directory for file operations
    ├── hello.txt
    ├── sample.txt
    └── test.md
```

## How It Works

### MCP Server (`server.py`)

1. Initializes an MCP server named "basic-fileserver"
2. Creates a `sandbox/` directory for secure file operations
3. Provides two tools:
   - `read_file`: Reads files from the sandbox directory
   - `write_file`: Writes files to the sandbox directory
4. All paths are resolved relative to the sandbox directory for security

### Gradio Interface (`app.py`)

1. Loads environment variables (including `GOOGLE_API_KEY`)
2. Creates a Gemini client using OpenAI-compatible API
3. Connects to the MCP server via stdio
4. Uses OpenAI Agents SDK to create an agent with MCP server access
5. Processes natural language prompts and executes file operations

## Security Notes

⚠️ **Important Security Considerations**:

- All file operations are restricted to the `sandbox/` directory
- Absolute paths are sanitized to prevent directory traversal
- The sandbox directory is automatically created if it doesn't exist
- Files in the sandbox directory are excluded from git (see `.gitignore`)

## Development

### Testing

You can test the server directly:

```bash
# Test reading a file
python -c "
import asyncio
from server import read_file_tool
result = asyncio.run(read_file_tool({'path': 'hello.txt'}))
print(result.content[0].text)
"
```

### Adding New Tools

To add new file operations, modify `server.py`:

1. Create a new async function (e.g., `async def delete_file_tool(...)`)
2. Add the tool to the `list_tools()` function
3. Add a handler in the `call_tool()` function

Remember to keep all operations within the sandbox directory for security.

## License

This project is provided as-is for use with the Model Context Protocol.
