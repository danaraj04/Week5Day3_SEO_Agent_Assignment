from ddgs import DDGS

def web_search(query: str) -> str:
    """
    Search the web for current information about the given query.

    Args:
        query: The search query.

    Returns:
        A formatted list of web search results.
    """

    try:
        results = DDGS().text(
            query,
            region="us-en",
            safesearch="moderate",
            max_results=5,
        )

        if not results:
            return "No search results found."

        output = []

        for index, result in enumerate(results, start=1):
            title = result.get("title", "")
            url = result.get("href", "")
            body = result.get("body", "")

            output.append(
                f"""
                SOURCE {index}
                Title: {title}
                URL: {url}
                Summary: {body}
                """
            )

        return "\n".join(output)

    except Exception as e:
        return f"Web search failed: {str(e)}"