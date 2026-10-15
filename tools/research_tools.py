import os

from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()


def search_web(
    query: str,
    max_results: int = 5,
) -> list[dict]:
    """
    Search the web and return structured results.

    Each result contains:
    - title
    - url
    - content
    """

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        raise ValueError(
            "TAVILY_API_KEY missing. Check your .env file."
        )

    if not query.strip():
        raise ValueError("Search query cannot be empty.")

    if not 1 <= max_results <= 10:
        raise ValueError(
            "max_results must be between 1 and 10."
        )

    client = TavilyClient(api_key=api_key)

    response = client.search(
        query=query,
        max_results=max_results,
        search_depth="basic",
    )

    results = []

    for item in response.get("results", []):
        url = item.get("url", "")
        content = item.get("content", "")

        if not url or not content:
            continue

        results.append({
            "title": item.get("title", "Untitled"),
            "url": url,
            "content": content,
        })

    return results


if __name__ == "__main__":
    query = "NASA scientific evidence of extraterrestrial life"

    search_results = search_web(
        query=query,
        max_results=3,
    )

    for index, result in enumerate(
        search_results,
        start=1,
    ):
        print(f"\n===== RESULT {index} =====")
        print("Title:", result["title"])
        print("URL:", result["url"])
        print("Content:", result["content"][:500])