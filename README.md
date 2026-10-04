# NEXUS

### From a goal to a plan, useful work, and a result you can download.

NEXUS is an AI productivity agent for turning learning material into practical outputs. Describe what you need, optionally upload a PDF, DOCX, or TXT file, and NEXUS plans the work, selects tools, runs them, checks quiz formatting, and brings the results together.

**Goal → Plan → Tools → Check → Answer**

Built with **Python, Streamlit, and Groq**. The default model is **GPT-OSS-20B**, served through Groq.

---

## Try it

Upload lecture notes and ask:

> Analyze these notes, create a 7-day study plan, and generate 10 multiple-choice questions.

NEXUS extracts the text, selects the relevant tools, shows the run progress, checks the quiz structure, and provides a downloadable result.

## What it does

- **Plans the task:** turns your goal into steps and selects from registered tools.
- **Reads documents:** extracts text from PDF, DOCX, and TXT uploads.
- **Creates study plans:** organizes topics, priorities, a 7-day schedule, and revision strategy.
- **Generates quizzes:** creates 10 MCQs with options, answers, and explanations; checks the format and attempts one repair if needed.
- **Writes reports:** produces an executive summary, findings, analysis, recommendations, and action items.
- **Shows its work:** displays the plan, selected tools, progress, document status, and quiz-format check.
- **Delivers the result:** shows the final response and lets you download it as Markdown.

## How it works

```mermaid
flowchart LR
    A[Goal + optional document] --> B[Extract document text]
    B --> C[LLM planner]
    C --> D[Validate tool choices]
    D --> E[Run registered Python tools]
    E --> F[Check quiz format]
    F --> G[LLM synthesis]
    G --> H[Answer + download]
