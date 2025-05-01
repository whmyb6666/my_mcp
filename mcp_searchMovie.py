import httpx
from typing import Dict, Any
from mcp.server import FastMCP
import requests

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzMDczM2U0MjJlYTI5ZGI0MGIzNjgzNWE1NjU1M2RhZiIsIm5iZiI6MTc0NDM1MjE2MS40NTEsInN1YiI6IjY3ZjhiM2ExN2Y3MGFjMWEyMWQ5MjQ0NiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.DfX7E6-dq2mXNrUiWAxV72ts-YXe_53s-bL7aXtPuWg"
}

async def addURL(data: Dict[str, Any]) -> Dict[str, Any]:
    if "results" in data:
        for movie in data["results"]:
            if movie.get("poster_path"):
                movie["poster_path"] = f"https://image.tmdb.org/t/p/original{movie['poster_path']}"
            if movie.get("backdrop_path"):
                movie["backdrop_path"] = f"https://image.tmdb.org/t/p/original{movie['backdrop_path']}"
    return data

app = FastMCP('movie_search_tool')

@app.tool()
async def search_movie(query: str = "the matrix", page: int = 1, language: str = "en-US") -> Dict[str, Any]:
    url = "https://api.themoviedb.org/3/search/movie"
    params = {"query": query, "include_adult": "false", "language": language, "page": page}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return await addURL(response.json())
        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    print("Server starting")
    app.run(transport='stdio')