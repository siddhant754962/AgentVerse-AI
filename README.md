
Loading older messages…
























































AgentVerse AI
AgentVerse AI is a multi-agent research and fact-checking
application built with LangGraph, LangChain, and Streamlit.
It combines web research with retrieval-augmented generation (RAG) to
help investigate a question, gather supporting context, evaluate factual
claims, and present a final report.

Research assistance, not a substitute for checking primary sources.
Verdicts depend on the quality and relevance of retrieved evidence.

Features
Multi-agent workflow: coordinates research, RAG, fact-checking,
and report generation.
Web research: retrieves web results using Tavily.
RAG pipeline: combines retrieved documents and research context
to ground responses in evidence.
PDF ingestion and retrieval: supports working with PDF content
through the RAG pipeline.
Vector search: uses ChromaDB for local vector storage.
LLM integration: uses Groq through the configured model
provider.
Embeddings: uses Hugging Face / Sentence Transformers
embeddings.
Claim assessment: labels claims based on the available evidence,
including supported, contradicted, or insufficient-evidence
outcomes.
Research report: organizes findings into a final report.
How it works
Research agent searches the web for relevant material.
RAG agent combines web results with retrieved document context
and prepares an evidence-grounded answer.
Fact-checker agent extracts factual claims and checks them
against the supplied evidence.
Conditional workflow can request additional research when the
evidence is insufficient, subject to the workflow's retry limit.
Report agent formats the findings into a final report.
Streamlit UI presents the workflow and its results.
A verdict should be interpreted in context: insufficient evidence does
not mean a claim is false. Review the cited sources and their relevance
before relying on a result.

Tech stack
Python 3.12+
Streamlit
LangChain
LangGraph
Groq
Tavily Search
Hugging Face / Sentence Transformers
ChromaDB
python-dotenv
Project structure
AgentVerse-AI/
├── agents/          # Research, RAG, fact-checking, and reporting agents
├── core/            # Shared LLM configuration and workflow state
├── graph/           # LangGraph workflow and routing
├── rag/             # Document ingestion and retrieval
├── tools/           # Web research tools
├── src/             # Supporting source code
├── app.py           # Streamlit application entry point
├── main.py           # Command-line / workflow entry point
├── pyproject.toml   # Project metadata and dependencies
├── requirements.txt # Pip dependency list
├── uv.lock          # Locked dependency versions for uv
└── .env             # Local secrets (create this yourself; do not commit it)
Some runtime folders, such as chroma_db/ and reports/, may be
created while the application runs and are intentionally not part of the
source repository.

Prerequisites
Python 3.12 or newer
API credentials for Groq and Tavily
Internet access for web research and model access
Setup
1. Clone the repository
git clone https://github.com/siddhant754962/AgentVerse-AI.git
cd AgentVerse-AI
2. Create and activate a virtual environment
Windows PowerShell

py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
If PowerShell blocks activation, you can run the environment's Python
directly or use the activation method appropriate for your system.

3. Install dependencies
Using pip:

python -m pip install --upgrade pip
pip install -r requirements.txt
If you use uv and prefer the lockfile-based setup:

uv sync
Use one installation method for the environment rather than mixing them
unnecessarily.

4. Configure environment variables
Create a .env file in the project root and add your own credentials:

GROQ_API_KEY=your_groq_api_key
MODEL_NAME=your_supported_groq_model
TAVILY_API_KEY=your_tavily_api_key
HF_TOKEN=your_hugging_face_token
Replace the example values with valid credentials and a model name
supported by your Groq account. Never commit .env or publish API keys
in screenshots, logs, or source code.

5. Run the application
Launch the Streamlit interface:

streamlit run app.py
If you want to run the separate workflow entry point, inspect main.py
for its expected arguments and invocation.

Configuration notes
GROQ_API_KEY: authenticates requests to Groq.
MODEL_NAME: selects the model configured by the project.
TAVILY_API_KEY: enables web search.
HF_TOKEN: Hugging Face token, if required by the selected
embedding/model resources.
The exact model identifier and credential requirements may vary with
provider availability and the models configured in the code.

Understanding claim verdicts
Verified / Supported: the retrieved evidence supports the claim.
False / Contradicted: the retrieved evidence directly conflicts
with the claim.
Unverified / Insufficient evidence: the available evidence is
not enough to establish whether the claim is true.
Disputed: evidence is mixed or sources materially disagree, if
the UI assigns this category.
A high number of search results does not automatically mean a claim is
true or false. Source quality, recency, context, and whether the source
directly addresses the claim all matter.

Troubleshooting
Missing API key: confirm that .env exists in the project root
and that variable names match the code.
No web results: check the Tavily key, internet connectivity, and
the search query.
Claims all appear unverified: inspect the raw fact-checker
output and verify that the UI correctly parses the returned JSON and
maps backend statuses to display verdicts.
Embedding or model download errors: check network access, Python
version, and whether the selected Hugging Face model is available.
Dependency installation issues: use Python 3.12+ and install
from either requirements.txt or uv.lock/pyproject.toml as
appropriate.
Security
Keep .env, API tokens, local vector databases, and generated
reports out of version control unless you deliberately intend to
share sanitized artifacts.
Rotate any API key that is accidentally exposed.
Check the provider's current terms, rate limits, and model
availability.
Roadmap ideas
Add automated tests for supported, contradicted, and
insufficient-evidence claims.
Improve source-quality scoring and show evidence excerpts beside
each verdict.
Add clearer handling for conflicting sources and stale information.
Add deployment-specific secrets configuration and a reproducible
smoke test.
Contributing
Issues and pull requests are welcome. For changes to the fact-checking
pipeline, include test cases that cover supported claims, contradicted
claims, and claims for which evidence is insufficient.

License
No license is specified here. Add a LICENSE file before presenting the
project as open source under a particular license.



⋮⋮⋮⋮
