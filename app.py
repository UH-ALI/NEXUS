import streamlit as st

from nexus.agent import AgentService
from nexus.config import load_settings
from nexus.llm import GroqLLM


st.set_page_config(page_title="NEXUS AI Agent", page_icon="🤖", layout="wide")
st.markdown(
    """
    <style>
    .stApp { background: radial-gradient(circle at 12% 5%, #29154c 0, transparent 28%),
        radial-gradient(circle at 90% 12%, #102b4b 0, transparent 25%), #080b18; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg,#100c20,#0b1324); }
    .nexus-logo { text-align:center; font-size:3rem; font-weight:900; letter-spacing:.12em;
        background:linear-gradient(90deg,#a78bfa,#60a5fa); color:transparent;
        background-clip:text; -webkit-background-clip:text; }
    .tagline { text-align:center; color:#a5b4fc; letter-spacing:.18em; font-size:.75rem; }
    [data-testid="stStatusWidget"] { border:1px solid #38345b; border-radius:14px; }
    div.stButton > button { border:1px solid #7958c8; border-radius:12px; }
    </style>
    """,
    unsafe_allow_html=True,
)

if "result" not in st.session_state:
    st.session_state.result = None
if "goal" not in st.session_state:
    st.session_state.goal = ""

with st.sidebar:
    st.markdown('<div class="nexus-logo">NEXUS</div><div class="tagline">AUTONOMOUS AI AGENT</div>', unsafe_allow_html=True)
    st.divider()
    st.subheader("Capabilities")
    st.markdown("Goal planning · PDF/DOCX/TXT extraction · Study plans · Quizzes · Reports · Result download")
    st.divider()
    st.subheader("Try an example")
    examples = [
        "Analyze my notes, create a 7-day study plan, and generate 10 MCQs.",
        "Summarize this document and produce a report with key findings.",
        "Help me prepare for an exam using the uploaded material.",
    ]
    for index, example in enumerate(examples):
        if st.button(example, key=f"example_{index}", use_container_width=True):
            st.session_state.goal = example

st.title("🤖 NEXUS AI Agent")
st.caption("Give NEXUS an outcome. Watch it plan, select tools, execute, and check its work.")

settings = load_settings()
status_cols = st.columns(3)
status_cols[0].metric("Agent", "Ready")
status_cols[1].metric("Provider", "Groq" if settings.groq_api_key else "Needs key")
status_cols[2].metric("Model", settings.groq_model)
if not settings.groq_api_key:
    st.info("Add GROQ_API_KEY to Streamlit Secrets or your environment to run NEXUS.")

goal = st.text_area(
    "What should NEXUS accomplish?",
    key="goal",
    height=110,
    placeholder="Example: Analyze my lecture notes, make a study plan, and create 10 practice questions.",
)
uploaded_file = st.file_uploader("Optional source material", type=["pdf", "docx", "txt"], help="Text-based PDF, DOCX, or TXT. Scanned PDFs need OCR first.")

run_col, _ = st.columns([1, 2])
run_agent = run_col.button("🚀 Run NEXUS", type="primary", use_container_width=True, disabled=not settings.groq_api_key)

if run_agent:
    if not goal.strip():
        st.warning("Enter a goal before running the agent.")
    else:
        try:
            model = GroqLLM(settings.groq_api_key, settings.groq_model)
            service = AgentService(model)
            with st.status("NEXUS is working…", expanded=True) as status:
                def show_event(event):
                    if event.kind == "plan":
                        st.write(f"**Plan ({event.details.get('planner_mode', 'unknown')}):**")
                        for step in event.details.get("plan", []):
                            st.write(f"- {step}")
                        st.write("**Selected tools:** " + ", ".join(event.details.get("tools", [])))
                    elif event.kind == "quality":
                        validation = event.details.get("validation", {})
                        st.write(f"{'✅' if validation.get('passed') else '⚠️'} {event.message}")
                    else:
                        icon = "⚠️" if event.kind == "tool_error" else "⚙️" if event.kind == "tool_start" else "✅" if event.kind == "tool_success" else "🧠"
                        st.write(f"{icon} {event.message}")

                result = service.run(goal.strip(), uploaded_file, on_event=show_event)
                status.update(label="NEXUS finished", state="complete", expanded=False)
            st.session_state.result = result
        except Exception as exc:
            st.error(f"NEXUS could not complete this run: {str(exc)[:400]}")

result = st.session_state.result
if result:
    st.divider()
    st.subheader("Run summary")
    st.caption(f"Planner: {result.planner_mode} · Tools: {', '.join(result.tools)} · {result.document_status}")
    with st.expander("Plan", expanded=False):
        for number, step in enumerate(result.plan, start=1):
            st.write(f"{number}. {step}")
    for tool_result in result.tool_results:
        with st.expander(f"{tool_result.name.title()} — {tool_result.status}"):
            st.write(tool_result.content)
            if "validation" in tool_result.details:
                validation = tool_result.details["validation"]
                if validation["passed"]:
                    st.success(f"Format check passed ({validation['question_count']} questions). This checks structure, not factual correctness.")
                else:
                    st.warning("Format check still has issues: " + " ".join(validation["problems"]))
    st.subheader("NEXUS result")
    st.markdown(result.final_result)
    st.download_button(
        "⬇️ Download result",
        data=result.final_result,
        file_name="nexus_result.md",
        mime="text/markdown",
        use_container_width=True,
    )

st.divider()
st.caption("NEXUS · Goal → Plan → Tools → Check → Synthesis")
