# """Chainlit UI — run with: chainlit run app.py"""
# import chainlit as cl
# from src.core.graph import research_agent

# STEP_LABELS = {
#     "planner": "🎯 Breaking down your question...",
#     "retriever": "🔍 Searching arXiv + Semantic Scholar...",
#     "synthesizer": "📝 Building research summary...",
#     "critic": "🔎 Fact-checking against sources...",
#     "format_answer": "✅ Formatting final answer...",
# }

# @cl.on_message
# async def main(message: cl.Message):
#     initial_state = {
#         "query": message.content, "sub_questions": [], "retrieved_papers": {},
#         "synthesis": "", "critique": "", "critique_passed": False,
#         "revision_count": 0, "messages": [], "final_answer": "",
#     }

#     final_answer = ""
#     async for step in research_agent.astream(initial_state):
#         node = list(step.keys())[0]
#         data = step[node]

#         if node in STEP_LABELS:
#             async with cl.Step(name=node) as s:
#                 s.output = STEP_LABELS[node]
#                 if node == "planner" and "sub_questions" in data:
#                     s.output += "\n" + "\n".join(f"  {i+1}. {q}" for i, q in enumerate(data["sub_questions"]))

#         if "final_answer" in data:
#             final_answer = data["final_answer"]

#     await cl.Message(content=final_answer or "Could not generate answer.").send()

"""
Nexus — Multi-Agent Research Assistant
Run: chainlit run app.py
"""
import chainlit as cl
from src.core.graph import research_agent
from src.core.llm import get_provider_info
import time


# ─── Starter prompts on empty chat ────────────────────

@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="LLM hallucination research",
            message="What are the latest approaches to reducing hallucination in large language models?",
            icon="/public/icons/brain.svg",
        ),
        cl.Starter(
            label="Compare transformer architectures",
            message="How do vision transformers compare to CNNs for medical image classification?",
            icon="/public/icons/compare.svg",
        ),
        cl.Starter(
            label="AI agents deep dive",
            message="What are the latest developments in AI agents and multi-agent systems in 2024-2026?",
            icon="/public/icons/agent.svg",
        ),
        cl.Starter(
            label="Federated learning in healthcare",
            message="What is federated learning and what are the main challenges of using it in healthcare?",
            icon="/public/icons/shield.svg",
        ),
    ]


# ─── Welcome message on chat start ────────────────────

@cl.on_chat_start
async def on_start():
    info = get_provider_info()
    welcome = (
        f"**Welcome to Nexus** — your multi-agent research assistant.\n\n"
        f"Ask me any complex research question and I'll deploy 4 specialized AI agents to:\n\n"
        f"1. **Plan** — Break your question into focused sub-queries\n"
        f"2. **Retrieve** — Search arXiv + Semantic Scholar for papers\n"
        f"3. **Synthesize** — Build a structured summary with citations\n"
        f"4. **Verify** — Fact-check every claim against sources\n\n"
        f"*Running on `{info['model']}` via {info['provider'].title()} — {info['cost']}*"
    )
    await cl.Message(content=welcome).send()


# ─── Agent step config ─────────────────────────────────

AGENT_CONFIG = {
    "planner": {
        "label": "Planner",
        "icon": "🎯",
        "msg": "Breaking down your question into focused sub-queries...",
    },
    "retriever": {
        "label": "Retriever",
        "icon": "🔍",
        "msg": "Searching arXiv and Semantic Scholar for papers...",
    },
    "synthesizer": {
        "label": "Synthesizer",
        "icon": "📝",
        "msg": "Building structured research summary with citations...",
    },
    "critic": {
        "label": "Critic",
        "icon": "🔎",
        "msg": "Fact-checking claims against source papers...",
    },
    "format_answer": {
        "label": "Formatter",
        "icon": "✅",
        "msg": "Packaging your verified research summary...",
    },
}


# ─── Handle user messages ──────────────────────────────

@cl.on_message
async def main(message: cl.Message):
    start_time = time.time()
    query = message.content

    initial_state = {
        "query": query,
        "sub_questions": [],
        "retrieved_papers": {},
        "synthesis": "",
        "critique": "",
        "critique_passed": False,
        "revision_count": 0,
        "messages": [],
        "final_answer": "",
    }

    final_answer = ""
    step_count = 0

    # Stream through each agent node
    async for step in research_agent.astream(initial_state):
        node_name = list(step.keys())[0]
        node_data = step[node_name]

        if node_name in AGENT_CONFIG:
            config = AGENT_CONFIG[node_name]
            step_count += 1

            async with cl.Step(
                name=f"{config['icon']} {config['label']}",
            ) as agent_step:
                agent_step.output = config["msg"]

                # Show sub-questions from planner
                if node_name == "planner" and "sub_questions" in node_data:
                    sub_qs = node_data["sub_questions"]
                    if sub_qs:
                        lines = "\n".join(
                            f"   {i+1}. {q}"
                            for i, q in enumerate(sub_qs)
                        )
                        agent_step.output = (
                            f"Decomposed into {len(sub_qs)} sub-questions:\n{lines}"
                        )

                # Show retriever count
                if node_name == "retriever" and "retrieved_papers" in node_data:
                    count = len(node_data["retrieved_papers"])
                    agent_step.output = (
                        f"Found papers for {count} sub-questions "
                        f"from arXiv + Semantic Scholar"
                    )

                # Show critic verdict
                if node_name == "critic":
                    passed = node_data.get("critique_passed", False)
                    rev = node_data.get("revision_count", 0)
                    if passed:
                        agent_step.output = "Verdict: PASS ✅"
                    else:
                        agent_step.output = (
                            f"Verdict: FAIL — revision {rev}/2"
                        )

        if "final_answer" in node_data:
            final_answer = node_data["final_answer"]

    # Send final answer with timing
    elapsed = time.time() - start_time
    footer = (
        f"\n\n---\n"
        f"*Nexus completed in {elapsed:.1f}s — "
        f"{step_count} agent steps*"
    )

    await cl.Message(
        content=(
            final_answer
            or "Could not generate a research summary."
        ) + footer,
    ).send()