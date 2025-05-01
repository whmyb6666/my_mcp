#!/usr/bin/env python3

# This script will read the movie_list.txt and display the data in a readable format.
from mcp_searchMovie.src.movie import use_mcp_tool


def main():
    # Read movies from file
    with open('movie_list.txt', 'r') as f:
        movies = [line.strip() for line in f]

    print("Movies from the list:")
    
    for movie_title in movies:
        # Fetch movie information using MCP server
        search_result = use_mcp_tool(
            "mcp-searchMovie",
            "search_movie",
            {"query": movie_title, "page": 1, "language": "en-US"}
        )

        if search_result:
            print(f"{movie_title}:")
            import json
            result = json.dumps(search_result['results'][0], indent=2)
            print(result)


if __name__ == "__main__":
    main()