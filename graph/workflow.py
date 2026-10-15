from langgraph.graph import END, START, StateGraph

from agents.fact_checker import fact_checker
from agents.rag_agent import rag_agent
from agents.report_agent import report_agent
from agents.research_agent import research_agent
from core.state import ResearchState


MAX_RESEARCH_ATTEMPTS = 2


def route_after_fact_check(state: ResearchState) -> str:
    """Decide whether more research is needed."""

    needs_more_research = state.get(
        "needs_more_research", False
    )

    research_attempts = state.get(
        "research_attempts", 0
    )

    if (
        needs_more_research
        and research_attempts < MAX_RESEARCH_ATTEMPTS
    ):
        print("\n[Workflow] More research is needed.")
        print(
            f"[Workflow] {research_attempts} research "
            f"attempt(s) completed."
        )
        return "research"

    print("\n[Workflow] Moving to the report agent.")
    return "report"


def build_workflow():
    """Create and compile the AgentVerse AI workflow."""

    builder = StateGraph(ResearchState)

    builder.add_node("research", research_agent)
    builder.add_node("rag", rag_agent)
    builder.add_node("fact_checker", fact_checker)
    builder.add_node("report", report_agent)

    builder.add_edge(START, "research")
    builder.add_edge("research", "rag")
    builder.add_edge("rag", "fact_checker")

    builder.add_conditional_edges(
        "fact_checker",
        route_after_fact_check,
        {
            "research": "research",
            "report": "report",
        },
    )

    builder.add_edge("report", END)

    return builder.compile()


# Compile the workflow once when this module is imported.
research_workflow = build_workflow()


def run_research(query: str) -> dict:
    """Execute the complete research workflow."""

    if not query or not query.strip():
        raise ValueError("Research query cannot be empty.")

    initial_state: ResearchState = {
        "query": query.strip(),
        "research_results": [],
        "web_results": [],
        "retrieved_context": [],
        "rag_answer": "",
        "verified_claims": [],
        "final_report": "",
        "needs_more_research": False,
        "research_attempts": 0,
    }

    return research_workflow.invoke(initial_state)


if __name__ == "__main__":
    question = input(
        "Enter your research question: "
    ).strip()

    try:
        result = run_research(question)

        print("\n" + "=" * 60)
        print("FINAL RESEARCH REPORT")
        print("=" * 60)

        print(
            result.get(
                "final_report",
                "No report was generated.",
            )
        )

        print("\nResearch attempts:")
        print(result.get("research_attempts", 0))

        print("\nFact-check results:")

        for claim in result.get("verified_claims", []):
            print(claim)

    except Exception as exc:
        print("\nWorkflow execution failed:", str(exc))
        raise