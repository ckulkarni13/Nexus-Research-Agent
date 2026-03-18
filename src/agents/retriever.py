"""Retriever: searches arXiv + Semantic Scholar for each sub-question."""
import signal
import logging
from src.tools.arxiv_search import search_arxiv
from src.tools.semantic_scholar import search_semantic_scholar
from src.tools.vector_store import cache_papers
from src.core.state import ResearchState


logger = logging.getLogger(__name__)


def retriever_node(state: ResearchState) -> dict:
    all_papers = {}

    for sub_q in state["sub_questions"]:
        papers_text = ""
        # arXiv (usually fast and reliable)
        try:
            arxiv_results = search_arxiv.invoke({"query": sub_q})
            papers_text += f"**arXiv:**\n{arxiv_results}\n\n"
        except Exception as e:
            logger.warning(f"arXiv failed for '{sub_q}': {e}")
            papers_text += "**arXiv:** Search failed\n\n"

        # Semantic Scholar — skip if it's been failing
        try:
            s2_results = search_semantic_scholar.invoke({"query": sub_q, "max_results": 3})
            papers_text += f"**Semantic Scholar:**\n{s2_results}"
        except Exception as e:
            logger.warning(f"S2 failed for '{sub_q}': {e}")
            papers_text += "**Semantic Scholar:** Unavailable"

        all_papers[sub_q] = papers_text

        # Cache for FAISS
        # try:
        #     cache_papers([papers_text[:2000]])
        # except Exception:
        #     pass

    return {"retrieved_papers": all_papers}