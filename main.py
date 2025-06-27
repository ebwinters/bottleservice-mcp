import argparse
import json
import os
import time
from mcp.server.fastmcp import FastMCP
import requests
import logging

mcp = FastMCP("BottleServiceMcp")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BottleServiceMcp")

PUBLIC_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh4Y2twZmtjYWJpYXVsc2hla3liIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA4NjIzNzEsImV4cCI6MjA2NjQzODM3MX0.Qt4Y07PiLxeZKeBwxV22DJJR9ITFn-5SOEvmHvc067k"
TOKEN_URL = "https://xxckpfkcabiaulshekyb.supabase.co/auth/v1/token?grant_type=password"
SHELF_BOTTLES_URL = "https://xxckpfkcabiaulshekyb.supabase.co/rest/v1/shelf_bottles?select=bottle_id"
BOTTLES_URL = "https://xxckpfkcabiaulshekyb.supabase.co/rest/v1/bottles?id=in.({ids})&select=name,category,subcategory"
TOKEN_CACHE = ".token_cache.json"

def get_token():
    """
    Retrieve and cache a Supabase access token using the password grant.

    This function first checks for a locally cached token and returns it if it is still valid.
    If no valid token is found, it requests a new one from the Supabase Auth API using the global USERNAME and PASSWORD variables.
    The new token is then cached locally with its expiry time for future use.

    Returns:
        str: The access token string to be used as a Bearer token in API requests.
    """
    # Check cache for a valid token
    if os.path.exists(TOKEN_CACHE):
        with open(TOKEN_CACHE, "r") as f:
            data = json.load(f)
            if data.get("expires_at", 0) > time.time():
                return data["access_token"]
    resp = requests.post(
        TOKEN_URL,
        headers={"apikey": PUBLIC_KEY, "Content-Type": "application/json"},
        json={"email": USERNAME, "password": PASSWORD}
    )
    resp.raise_for_status()
    token_data = resp.json()
    token_data["expires_at"] = time.time() + token_data.get("expires_in", 3600) - 60
    with open(TOKEN_CACHE, "w") as f:
        json.dump(token_data, f)
    return token_data["access_token"]

from typing import Literal

BottleCategory = Literal[
    "",
    "Whiskey",
    "Rum",
    "Gin",
    "Vodka",
    "Tequila",
    "Brandy",
    "Liqueur",
    "Mezcal",
    "Schnapps",
    "Absinthe",
    "Other",
    "Bitters",
    "Vermouth",
    "Fruits/Juices",
    "Syrups",
    "Mixers",
]

@mcp.tool()
def get_user_bottles(category: BottleCategory = ""):
    """
    Retrieve all bottles for the user on their bar shelf.

    Args:
        category (str, optional): The category of bottle to filter by. Defaults to "".

    Returns:
        list: List of bottle details, each containing name, category, and subcategory.
    """
    token = get_token()
    resp = requests.get(
        SHELF_BOTTLES_URL,
        headers={"apikey": PUBLIC_KEY, "Authorization": f"Bearer {token}"}
    )

    resp.raise_for_status()
    ids = [item["bottle_id"] for item in resp.json()]
    logger.info(f"Retrieved {len(ids)} bottle IDs from shelf_bottles")
    if not ids:
        return []
    ids_str = ",".join(map(str, ids))
    url = BOTTLES_URL.format(ids=ids_str)
    if category:
        url += f"&category=eq.{category}"
    resp = requests.get(
        url,
        headers={"apikey": PUBLIC_KEY, "Authorization": f"Bearer {token}"}
    )
    resp.raise_for_status()
    bottles = resp.json()
    formatted = [
        f"{bottle['name']} ({bottle['category']}/{bottle['subcategory']})"
        for bottle in bottles
    ]
    return "\n".join(formatted)

def main():
    parser = argparse.ArgumentParser(description="BottleService MCP server")
    parser.add_argument("--username", type=str, required=True, help="Supabase username (email)")
    parser.add_argument("--password", type=str, required=True, help="Supabase password")
    args = parser.parse_args()

    global USERNAME, PASSWORD
    USERNAME = args.username
    PASSWORD = args.password
    print(f"Starting BottleService MCP server for user: {USERNAME}")
    logger.info(f"Starting BottleService MCP server for user: {USERNAME}")
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()