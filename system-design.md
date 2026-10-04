# NEXUS System Design

## Design goals

Preserve the working Streamlit + Groq product while making responsibilities explicit, observable, and easy to change. Keep orchestration as a small Python control loop rather than introducing a framework.

## Architecture

```text
Streamlit UI
  ├─ Goal + optional upload
  ├─ Live status / plan / selected tools / final result / download
  └─ calls AgentService.run(goal, upload, on_event)
       ├─ DocumentService: safe format dispatch + bounded text extraction
       ├─ Planner: Groq JSON plan → schema + allow-list validation → fallback
       ├─ ToolRegistry: fixed mapping of names to local tool functions
       │    ├─ Study tool
       │    ├─ Quiz tool → structural check → one bounded repair
       │    └─ Report tool
       └─ Synthesizer: tool results + failures → final user response
```

The model proposes an intent and tool names. Python validates and executes those names from a fixed registry. The model never receives an executable code tool, shell, or arbitrary dispatch capability.

## Request lifecycle

1. UI validates the goal and emits a request-start event.
2. If a file exists, document service checks its extension, extracts text, and enforces a character budget. Extraction errors are recorded and shown.
3. Planner receives the goal and whether usable document content exists. Its JSON is parsed, normalized, and restricted to registered tools. On failure, deterministic keyword routing produces a clearly labeled fallback plan.
4. Selected tools run sequentially. Each emits start, success, or failure events and returns a structured result (`status`, `content`, optional `details`).
5. Quiz results undergo deterministic structural validation. A failed quiz may receive one repair prompt; the final validation result is surfaced.
6. Synthesizer receives the original goal, plan, tool statuses, and bounded results. It must disclose unavailable source content and tool failures that affect the outcome.
7. UI stores the structured run and renders the plan, actual events, final result, quality status, and download.

## Module boundaries

- `app.py`: Streamlit presentation and session state only.
- `nexus/config.py`: settings and safe secret lookup.
- `nexus/agent.py`: orchestration lifecycle and event emission.
- `nexus/llm.py`: Groq adapter, model calls, prompt-size limits.
- `nexus/planner.py`: planner prompt, parser, schema validation, deterministic fallback.
- `nexus/registry.py`: fixed tool registry and dispatch.
- `nexus/documents.py`: PDF/DOCX/TXT extraction and input checks.
- `nexus/tools/`: focused study, quiz, report implementations and quiz validation.
- `nexus/types.py`: typed result and event structures.

## Contracts

Tool names are a closed set: `study`, `quiz`, `report`, and `document`. Tool results are structured and JSON-safe. Planner output has `plan: list[str]` and `tools: list[str]`; malformed or unknown entries are rejected or filtered before dispatch. Agent events are plain text plus a stable event kind so UI rendering does not infer progress from prose.

## Reliability and failure handling

- Missing credentials are a configuration error presented in the UI.
- Unsupported, empty, encrypted, or unextractable files produce explicit document status; the system does not claim to have analyzed them.
- A planner error activates deterministic routing and is labeled as fallback behavior.
- Individual tool failures are captured; other selected tools can still complete.
- Synthesis failure returns a readable summary of successful tool output rather than a false success message.
- Model calls are bounded; only one quiz repair attempt is allowed.

## Security and privacy

- Credentials are read from Streamlit secrets or environment variables and are never displayed.
- Uploaded text is untrusted data. Prompts explicitly instruct the model to analyze it as content and ignore instructions embedded in it.
- Tool dispatch is allow-listed and implemented in Python; no model-selected code execution.
- File type is checked by extension and extraction library; upload size is bounded in the UI and document text is capped before model calls.
- Outputs are rendered as Markdown, with no custom HTML rendering of model output.

## Key decisions

1. Keep one orchestrating agent: the workflow is sequential and well-scoped; multi-agent coordination adds latency and failure modes without helping the demo.
2. Keep direct document context for now: uploaded text is capped and passed to tools. RAG is deferred until document size and retrieval needs justify it.
3. Use deterministic output checks for quiz structure; use the LLM only for generation/repair, not as the sole claim of correctness.
4. Preserve the current provider/model defaults while centralizing configuration so future provider changes are localized.

## Main tradeoffs

- Sequential tools are predictable and easy to demo but can be slower than parallel execution.
- Character limits are simple but not exact token budgets; the model API remains authoritative about context limits.
- Structural checks improve format reliability but do not establish correctness of answers or factual claims.
