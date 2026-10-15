from agents.report_agent import report_agent


initial_state = {
    "query": "What does an unidentified observation prove?",
    "research_results": [
        (
            "The available research does not establish that "
            "an unidentified observation has an extraterrestrial origin."
        )
    ],
    "web_results": [],
    "retrieved_context": [
        {
            "source_type": "web",
            "title": "Example Evidence",
            "url": "https://example.com/evidence",
            "content": (
                "An unidentified observation has not yet "
                "been conclusively explained."
            ),
        }
    ],
    "rag_answer": (
        "An unidentified observation alone does not establish "
        "an extraterrestrial origin."
    ),
    "verified_claims": [
        (
            '{"claim": "An unidentified observation alone does not '
            'establish an extraterrestrial origin.", '
            '"status": "supported", '
            '"explanation": "The supplied evidence does not establish '
            'an extraterrestrial origin.", '
            '"sources": [1]}'
        )
    ],
    "final_report": "",
    "needs_more_research": False,
    "research_attempts": 1,
}


result = report_agent(initial_state)

print("\n========== FINAL RESEARCH REPORT ==========\n")
print(result["final_report"])

# Save the report locally.
with open(
    "research_report.md",
    "w",
    encoding="utf-8",
) as file:
    file.write(result["final_report"])

print("\nReport saved to research_report.md")