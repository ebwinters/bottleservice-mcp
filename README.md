<img src="https://raw.githubusercontent.com/ebwinters/bottleservice/refs/heads/main/src/assets/bottle_logo.jpg" width="100">
This MCP server works with your bottle collection from the [bottle service web app](https://bottleservice.vercel.app/#). Make an account to add bottles to your bar shelf


## Sample Prompts
- Suggest a drink I can make with my tequila and amaro bottles.
- How many bottles of whiskey do I own?
- Show me all my gin bottles, sorted by how full they are.
- What is a good sweet drink I can make for someone who likes citrus?

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
