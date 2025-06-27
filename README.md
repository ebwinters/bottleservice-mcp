This MCP server works with your bottle collection from the [bottle service web app](https://bottleservice.vercel.app/#). Make an account to add bottles to your bar shelf

## Quick Setup
1. Clone repo

2. Add this to your MCP server config (replace with your username and password):
   ```json
    "bottleservice-mcp-local": {
        "type": "stdio",
        "command": "uv",
        "args": [
            "--directory",
            "C:\\....\\bottleservice-mcp",
            "run",
            "main.py",
            "--username",
            "BOTTLESERVICE_USERNAME",
            "--password",
            "BOTTLESERVICE_PASSWORD"
        ]
    }
    ```
