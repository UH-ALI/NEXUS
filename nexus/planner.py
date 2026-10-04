import json
import re


TOOL_DESCRIPTIONS = {
    "document": "Include extracted document context in the final synthesis.",
    "study": "Create a structured study plan and 7-day schedule.",
    "quiz": "Generate a 10-question multiple-choice quiz.",
    "report": "Create a structured report with findings and actions.",
}
ALLOWED_TOOLS = tuple(TOOL_DESCRIPTIONS)


def fallback_plan(goal: str, has_document: bool) -> tuple[list[str], list[str]]:
    words = set(re.findall(r"[a-z]+", goal.lower()))
    tools = []
    if has_document and words.intersection({"document", "file", "pdf", "notes", "uploaded", "analyze", "analyse", "summarize", "summary"}):
        tools.append("document")
    if words.intersection({"study", "learn", "schedule", "plan", "exam", "prepare"}):
        tools.append("study")
    if words.intersection({"quiz", "mcq", "question", "questions", "test"}):
        tools.append("quiz")
    if words.intersection({"report", "analysis", "analyze", "analyse", "summary", "summarize"}):
        tools.append("report")
    if not tools:
        tools = ["report"]
    if has_document and "document" not in tools:
        tools.insert(0, "document")
    plan = ["Understand the requested outcome", "Select registered tools", "Run the selected tools", "Synthesize the results"]
    return plan, list(dict.fromkeys(tools))


def make_plan(goal: str, has_document: bool, llm) -> tuple[list[str], list[str], str]:
    prompt = f"""Plan work for the user's goal. Choose only from the registered tools below.
Goal: {goal}
Usable uploaded document: {"yes" if has_document else "no"}
Registered tools: {json.dumps(TOOL_DESCRIPTIONS)}
Return JSON only with this schema: {{"plan": ["step"], "tools": ["registered_name"]}}.
Use a short ordered plan and only tools that contribute to the goal."""
    try:
        raw = llm.complete("You are a precise planner. Return valid JSON and never invent tool names.", prompt)
        match = re.search(r"\{[\s\S]*\}", raw)
        if not match:
            raise ValueError("Planner response was not JSON.")
        data = json.loads(match.group(0))
        plan = data.get("plan")
        tools = data.get("tools")
        if not isinstance(plan, list) or not all(isinstance(step, str) for step in plan):
            raise ValueError("Planner returned an invalid plan.")
        if not isinstance(tools, list) or not all(isinstance(tool, str) for tool in tools):
            raise ValueError("Planner returned invalid tool names.")
        selected = list(dict.fromkeys(tool for tool in tools if tool in ALLOWED_TOOLS))
        if not selected:
            raise ValueError("Planner did not select a registered tool.")
        steps = [step.strip() for step in plan if step.strip()][:8]
        if not steps:
            raise ValueError("Planner returned an empty plan.")
        return steps, selected, "llm"
    except Exception:
        plan, tools = fallback_plan(goal, has_document)
        return plan, tools, "fallback"
