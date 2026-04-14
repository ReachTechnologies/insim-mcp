# Contributing to insim-mcp

Thanks for your interest in contributing to insim-mcp! This guide will help you get set up.

## Development Setup

### Prerequisites

- Python 3.10+
- An inSIM account with API access ([insim.app](https://www.insim.app))

### Install from source

```bash
git clone https://github.com/ReachTechnologies/insim-mcp.git
cd insim-mcp
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -e .
```

### Run the server locally

```bash
export INSIM_LOGIN="your@email.com"
export INSIM_ACCESS_KEY="your_access_key"
insim-mcp
```

The server runs on stdio by default (MCP standard transport).

## Adding a New Tool

1. Edit `src/insim_mcp/server.py`
2. Add a new function with `@mcp.tool()` decorator
3. Use `_api_post()` helper for API calls
4. Return `json.dumps(result)` for consistent output
5. Add type hints and docstring (used by MCP for tool description)

### Example

```python
@mcp.tool()
def my_new_tool(param: str, limit: int = 10) -> str:
    """Description shown to AI agents.

    Args:
        param: What this parameter does.
        limit: Maximum results to return.
    """
    return json.dumps(_api_post("/api/v2/endpoint", {"param": param, "limit": limit}))
```

## Code Style

- Type hints on all function parameters
- Docstrings with Args section (MCP uses these for tool descriptions)
- All API calls go through `_api_post()` helper
- Return JSON strings from tools

## Pull Request Process

1. Fork the repo and create a feature branch
2. Make your changes
3. Test with a real MCP client (Claude Code, Cursor, etc.)
4. Submit a PR with a clear description

## Reporting Issues

Open an issue at [github.com/ReachTechnologies/insim-mcp/issues](https://github.com/ReachTechnologies/insim-mcp/issues) with:

- What you expected vs. what happened
- Which MCP client you're using
- Your Python version (`python --version`)

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.
