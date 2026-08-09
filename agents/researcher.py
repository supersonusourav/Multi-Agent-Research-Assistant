import re
from urllib.parse import urlparse
from tools.search import search


def researcher_agent(state):
    """
    Research Agent
    Executes web searches and stores citations cleanly.
    """
    research_results = []
    citations = []
    seen_urls = set()
    domains = set()
    total_sources = 0

    # Parse queries line-by-line
    questions = [q.strip() for q in state["sub_questions"].splitlines() if q.strip()]

    for question in questions:
        # Strip any remaining numbers/bullets if the LLM outputted them
        cleaned_question = re.sub(r"^\s*(\d+[\.\)]\s*|[-*•]\s*)", "", question).strip()

        if not cleaned_question:
            continue

        print(f"\nSearching: {cleaned_question}")
        sources = search(cleaned_question)
        print(f"Sources returned: {len(sources)}")

        filtered_sources = []

        for source in sources:
            if not isinstance(source, dict):
                continue

            url = source.get("url", "").strip()

            if url and url in seen_urls:
                continue

            if url:
                seen_urls.add(url)
                netloc = urlparse(url).netloc
                if netloc:
                    domains.add(netloc)

            cleaned_item = {
                "title": source.get("title", "Untitled"),
                "url": url,
                "content": source.get("content", ""),
            }

            filtered_sources.append(cleaned_item)

            if url:
                citations.append(
                    {
                        "title": cleaned_item["title"],
                        "url": cleaned_item["url"],
                    }
                )
            total_sources += 1

        print(f"Unique sources kept for question: {len(filtered_sources)}")

        research_results.append(
            {
                "question": cleaned_question,
                "sources": filtered_sources,
            }
        )

    state["research"] = research_results
    state["citations"] = citations

    state["statistics"].update(
        {
            "questions": len(research_results),
            "sources": total_sources,
            "unique_domains": len(domains),
        }
    )

    return state