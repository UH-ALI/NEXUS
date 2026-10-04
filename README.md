# NEXUS — Autonomous AI Productivity Agent

NEXUS accepts a goal and optional PDF, DOCX, or TXT material, plans the work, selects from fixed local tools, runs them, checks quiz structure, and synthesizes a downloadable response. Built with Streamlit, Python, and the Groq API.

## Run locally

Requires Python 3.10 or newer and a Groq API key.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .streamlit\secrets.toml.example .streamlit\secrets.toml
```

Put your own key in `.streamlit/secrets.toml` (never commit or share that file):

```toml
GROQ_API_KEY = "your-key"
GROQ_MODEL = "openai/gpt-oss-20b"
```

Run the app from this repository root:

```powershell
streamlit run app.py
```

## Project layout

```text
nexus-agent/
├── app.py                    # Streamlit UI
├── nexus/                    # Agent, planner, provider, document service, tools
├── .streamlit/config.toml    # Safe UI settings
├── .streamlit/secrets.toml.example
├── requirements.txt
├── PRD.md
├── system-design.md
├── SECURITY.md
├── DEPLOYMENT.md
└── POST-SUBMISSION.md
```

## Current scope

NEXUS uses one orchestrating agent and an allow-listed set of Python tools. It does not currently use RAG, embeddings, OCR, web search, persistent memory, or a multi-agent framework. Quiz validation checks output structure, not factual correctness. See [the PRD](PRD.md), [system design](system-design.md), and [security notes](SECURITY.md).
