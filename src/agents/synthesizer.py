"""Synthesizer: builds structured summary from retrieved papers."""
from langchain_core.prompts import ChatPromptTemplate
from src.core.llm import get_llm
from src.core.state import ResearchState
from src.config.prompts import SYNTHESIZER_SYSTEM

prompt = ChatPromptTemplate.from_messages([
    ("system", SYNTHESIZER_SYSTEM),
    ("human", "Original query: {query}\n\nRetrieved papers:\n{papers}\n\nCreate synthesis:")
])


def synthesizer_node(state: ResearchState) -> dict:
    llm = get_llm(temperature=0.4)

    papers_text = ""
    for sub_q, papers in state["retrieved_papers"].items():
        papers_text += f"\n### {sub_q}\n{papers}\n"

    chain = prompt | llm
    response = chain.invoke({"query": state["query"], "papers": papers_text[:8000]})
    return {"synthesis": response.content}