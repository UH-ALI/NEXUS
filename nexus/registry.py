from nexus.tools.report import create_report
from nexus.tools.quiz import generate_quiz, repair_quiz, validate_quiz
from nexus.tools.study import create_study_plan
from nexus.types import ToolResult


class ToolRegistry:
    """Fixed local dispatch table; planner output cannot call arbitrary code."""

    def __init__(self):
        self._tools = {"study", "quiz", "report", "document"}

    @property
    def names(self) -> set[str]:
        return set(self._tools)

    def execute(self, name: str, goal: str, document_text: str, llm) -> ToolResult:
        if name not in self._tools:
            return ToolResult(name=name, status="error", content="Unknown tool was blocked.")
        try:
            if name == "study":
                content = create_study_plan(goal, document_text, llm)
                return ToolResult(name, "success", content)
            if name == "quiz":
                content = generate_quiz(goal, document_text, llm)
                check = validate_quiz(content)
                attempts = 0
                if not check["passed"]:
                    attempts = 1
                    content = repair_quiz(content, check["problems"], llm)
                    check = validate_quiz(content)
                return ToolResult(name, "success", content, {"validation": check, "repair_attempts": attempts})
            if name == "report":
                content = create_report(goal, document_text, llm)
                return ToolResult(name, "success", content)
            if name == "document":
                if not document_text:
                    return ToolResult(name, "error", "No readable document text was available.")
                return ToolResult(name, "success", f"Extracted document context is available to the selected tools ({len(document_text)} characters).")
        except Exception as exc:
            return ToolResult(name=name, status="error", content=str(exc)[:500])
        return ToolResult(name=name, status="error", content="Tool failed without a result.")
