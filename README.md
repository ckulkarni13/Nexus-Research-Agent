# Nexus Research Agent: Multi-Agent Research & Verification System

An autonomous, multi-agent research pipeline designed to transform raw scientific queries into verified, high-quality research summaries. This system leverages **LangGraph** for stateful orchestration and **CrewAI** for agentic role-playing.

---

## 📌 Project Overview
The **Nexus Research Agent** is built to solve the "hallucination" and "relevance" challenges in AI-driven research. Unlike linear search tools, this system implements a **4-agent research pipeline** with a **conditional critic feedback loop**. The agents work collaboratively to search, analyze, and verify findings from **arXiv** and **Semantic Scholar**, ensuring that the final output is both scientifically grounded and deeply insightful.

## 🛠 Tech Stack
* **Orchestration:** LangGraph (State management and cyclical workflows).
* **Agentic Framework:** CrewAI.
* **Data Sources:** arXiv API, Semantic Scholar API.
* **Language Models:** OpenAI GPT-4o / Claude 3.5 Sonnet.
* **Interface:** Streamlit (Autonomous Research Dashboard).

## 🏗 System Architecture & Agent Roles
The pipeline is governed by a cyclic graph that manages transitions between four specialized agents:

1.  **The Researcher:** Executes complex queries across academic databases to find the most recent and relevant papers.
2.  **The Analyst:** Processes retrieved papers to extract core methodologies, results, and limitations.
3.  **The Critic:** Evaluates the Analyst’s summary for depth and technical accuracy. If the quality is insufficient, it triggers a feedback loop for further research or analysis.
4.  **The Verifier:** Cross-references the final report against the source metadata to eliminate hallucinations and ensure 100% groundedness.

## 🚀 Key Features
* **Conditional Feedback Loops:** Implements a logic-based "Critic" stage that can send the workflow back to the research phase if initial findings are weak.
* **Multi-Source Ingestion:** Simultaneously queries and merges insights from multiple academic repositories.
* **Hallucination Mitigation:** Dedicated verification step that acts as a final filter before user delivery.
* **Stateful Memory:** Uses LangGraph's persistent state to maintain context across complex, multi-turn research tasks.

## 📂 Repository Structure
* `agents/`: Definitions for Researcher, Analyst, Critic, and Verifier agents.
* `tools/`: Custom wrappers for arXiv and Semantic Scholar APIs.
* `graph/`: LangGraph workflow logic and state transitions.
* `app.py`: Streamlit-based UI for real-time research monitoring.

---
*Developed by [Chinmay Kulkarni](https://github.com/ckulkarni13)*
