# NEXUS Product Requirements

## Product

NEXUS is a single-user AI productivity agent that turns a goal and optional uploaded learning material into a study plan, quiz, document summary, or structured report. Its distinguishing behavior is an explicit plan → tool selection → tool execution → checked synthesis workflow.

## Users and need

Primary user: a student or knowledge worker who has a document and wants a useful, structured output without manually prompting several separate tools.

## Goals

- Preserve the current reliable Streamlit interaction and Groq model provider.
- Make the agent's selected plan, tools, and actual execution progress visible.
- Produce downloadable results and useful error messages.
- Avoid implying that outputs were checked when validation did not run or failed.
- Keep installation and deployment simple enough for a small hackathon project.

## User stories

1. As a user, I can describe an outcome and optionally upload PDF, DOCX, or TXT material.
2. As a user, I can see the plan and selected tools before or as they run.
3. As a user, I can receive a study plan, a quiz, a report, or a combination selected for my goal.
4. As a user, I can distinguish document extraction, model, and output-validation failures.
5. As a user, I can download the final response as a text file.

## Functional requirements

- Accept a non-empty goal and optional PDF, DOCX, or TXT upload.
- Extract text from supported formats and reject unsupported or empty/unreadable inputs with a clear status.
- Ask the configured Groq chat model for a plan using only registered tools.
- Validate the planner response and use a deterministic keyword-based fallback if planning fails.
- Execute selected tools through an explicit local registry; the model cannot invoke arbitrary Python or shell commands.
- Generate study plans, quizzes, and structured reports using the request and available document context.
- Validate quiz structure (question count and four labeled options) and make at most one repair call when validation fails.
- Synthesize tool results into a final response while preserving errors and source limitations.
- Stream actual workflow events to the Streamlit status view and retain the last result for download.

## Non-functional requirements

- Python 3.10+ and a small dependency set: Streamlit, Groq, pypdf, python-docx.
- API credentials come from Streamlit secrets or supported environment variables; never commit credentials.
- External model calls have bounded prompt size and a bounded number of repair calls.
- Failures in an optional tool should not crash the whole UI or be described as successful completion.
- No vector database, embeddings, autonomous filesystem access, or multi-agent framework in this release.

## Success criteria

- A user can complete the example workflow (upload lecture notes → request a study plan and 10 MCQs → see the tool trace → download results).
- The UI reports actual plan/tool/extraction/validation state.
- Invalid planner output cannot dispatch unknown tools.
- Quiz output visibly indicates whether structural validation passed.
- The app starts with a valid Groq key and reports missing configuration without a traceback.

## Out of scope

Traditional RAG, embeddings, persistent memory, user accounts, web search, calendars/email, multi-agent collaboration, voice, and autonomous writes to external systems.

## Risks and assumptions

- Model availability, rate limits, and latency depend on Groq and the selected model.
- Structural validation can catch formatting defects, not guarantee factual correctness.
- Document extraction is text extraction only; scanned image OCR is not included.
- Uploaded content may contain prompt injection; it is treated as untrusted source data and is never allowed to redefine system behavior or tool permissions.
