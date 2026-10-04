from dataclasses import dataclass, field
from typing import Any, Callable, Literal

EventKind = Literal["info", "plan", "tool_start", "tool_success", "tool_error", "quality"]


@dataclass
class AgentEvent:
    kind: EventKind
    message: str
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolResult:
    name: str
    status: Literal["success", "error"]
    content: str = ""
    details: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {"name": self.name, "status": self.status, "content": self.content, "details": self.details}


@dataclass
class RunResult:
    goal: str
    plan: list[str]
    tools: list[str]
    tool_results: list[ToolResult]
    final_result: str
    planner_mode: Literal["llm", "fallback"]
    document_status: str
    events: list[AgentEvent]
    quality: dict[str, Any] = field(default_factory=dict)


EventCallback = Callable[[AgentEvent], None]
