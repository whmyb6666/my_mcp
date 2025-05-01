#!/usr/bin/env python3

# Simple test to confirm use_mcp_tool function works correctly.
from mcp_searchMovie.src.movie import Movie, use_mcp_tool


def main():
    # Test call to MCP server using a simple query
    search_result = use_mcp_tool(
        "mcp-searchMovie",
        "search_movie",
        {"query": "A Minecraft Movie", "page": 1, "language": "en-US"}
    )

    if search_result:
        print(json.dumps(search_result['results'][0], indent=2))  # Assuming the search returns a list of dictionaries


if __name__ == "__main__":
    main()