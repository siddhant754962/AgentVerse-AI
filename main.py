from datetime import datetime
from pathlib import Path

from graph.workflow import run_research


REPORTS_DIR = Path("reports")


def save_report(
    report: str,
    query: str,
) -> Path:
    """Save the generated research report as Markdown."""

    REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    report_path = REPORTS_DIR / (
        f"research_report_{timestamp}.md"
    )

    report_content = (
        f"# AgentVerse AI Research Report\n\n"
        f"**Research Question:** {query}\n\n"
        f"**Generated At:** "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"---\n\n"
        f"{report}\n"
    )

    report_path.write_text(
        report_content,
        encoding="utf-8",
    )

    return report_path


def main() -> None:
    """Run AgentVerse AI from the terminal."""

    print("=" * 60)
    print("             AGENTVERSE AI")
    print("      Multi-Agent Research System")
    print("=" * 60)

    print(
        "\nAsk a research question. "
        "Type 'exit' to quit."
    )

    while True:
        query = input(
            "\nEnter your research question: "
        ).strip()

        if query.lower() in {"exit", "quit"}:
            print("\nGoodbye, bhai! 👋")
            break

        if not query:
            print(
                "Please enter a valid research question."
            )
            continue

        try:
            print(
                "\n[AgentVerse] Research started..."
            )

            result = run_research(query)

            report = result.get(
                "final_report",
                "",
            )

            if not report.strip():
                print(
                    "\nNo final report was generated."
                )
                continue

            report_path = save_report(
                report=report,
                query=query,
            )

            print("\n" + "=" * 60)
            print("              RESEARCH REPORT")
            print("=" * 60)

            print(report)

            print("\n" + "=" * 60)
            print("Research attempts:", result.get(
                "research_attempts",
                0,
            ))

            print(
                "Report saved at:",
                report_path.resolve(),
            )

            print("=" * 60)

        except Exception as exc:
            print(
                f"\n[AgentVerse] Error: {exc}"
            )

            print(
                "Check your API keys, model configuration, "
                "network connection, and error traceback."
            )


if __name__ == "__main__":
    main()