"""Semantic Scholar search — free, no API key, 100 req/sec."""
from semanticscholar import SemanticScholar
from langchain_core.tools import tool
from src.config.settings import settings


@tool
def search_semantic_scholar(query: str, max_results: int = 0) -> str:
    """Search Semantic Scholar for papers with citation counts."""
    if max_results == 0:
        max_results = settings.scholar_max_results

    sch = SemanticScholar(timeout=5)  # 5 second timeout instead of default

    try:
        results = sch.search_paper(query, limit=max_results,
            fields=["title", "abstract", "year", "citationCount", "url", "authors"])
    except Exception:
        return "Semantic Scholar temporarily unavailable."

    if not results:
        return "No papers found."

    output = []
    for p in results[:max_results]:
        authors = ", ".join(str(a.name) if hasattr(a, "name") else str(a) for a in (p.authors or [])[:3])
        output.append(
            f"Title: {p.title}\n"
            f"Authors: {authors}\n"
            f"Year: {p.year} | Citations: {p.citationCount}\n"
            f"Abstract: {(p.abstract or 'N/A')[:400]}\n"
            f"URL: {p.url}"
        )
    return "\n\n---\n\n".join(output)