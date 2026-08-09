import pprint
from dotenv import load_dotenv
from langchain_tavily import TavilySearch

load_dotenv()

# Initialize Tavily Tool
tavily = TavilySearch(max_results=3)


def search(query: str) -> list[dict]:
    """
    Search the web using Tavily and normalize output.
    """
    try:
        # 1. Try dict input payload first (standard in langchain-tavily)
        try:
            response = tavily.invoke({"query": query})
        except Exception:
            # Fallback to direct string query if dict invocation fails
            response = tavily.invoke(query)

        print("\n" + "=" * 80)
        print(f"QUERY: {query}")
        print(f"TYPE : {type(response)}")
        print("=" * 80 + "\n")

        results = []

        # Handle string response (if returned as JSON string)
        if isinstance(response, str):
            import json
            try:
                response = json.loads(response)
            except Exception:
                pass

        # Handle dictionary response
        if isinstance(response, dict):
            if "results" in response:
                results = response["results"]
            elif "url" in response:
                results = [response]

        # Handle list response
        elif isinstance(response, list):
            results = response

        cleaned_results = []

        for item in results:
            # Format A: Dictionary
            if isinstance(item, dict):
                url = item.get("url", "").strip()
                title = item.get("title", "Untitled")
                content = (
                    item.get("content")
                    or item.get("raw_content")
                    or item.get("snippet")
                    or ""
                )

            # Format B: LangChain Document object
            elif hasattr(item, "page_content"):
                content = getattr(item, "page_content", "")
                metadata = getattr(item, "metadata", {})
                url = metadata.get("url", "").strip()
                title = metadata.get("title", "Untitled")

            else:
                continue

            if url or content:
                cleaned_results.append(
                    {
                        "title": title or "Untitled",
                        "url": url,
                        "content": content,
                    }
                )

        print(f"Retrieved {len(cleaned_results)} valid results for query: '{query}'")
        return cleaned_results

    except Exception as e:
        print("\n" + "=" * 80)
        print("TAVILY SEARCH ERROR:", e)
        print("=" * 80 + "\n")
        return []