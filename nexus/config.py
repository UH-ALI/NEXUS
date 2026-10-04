import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    groq_api_key: str
    groq_model: str = "openai/gpt-oss-20b"
    max_document_chars: int = 24000
    max_result_chars: int = 24000


def _streamlit_secret(name: str) -> str:
    try:
        import streamlit as st

        return str(st.secrets.get(name, "") or "")
    except Exception:
        return ""


def load_settings() -> Settings:
    return Settings(
        groq_api_key=os.getenv("GROQ_API_KEY") or _streamlit_secret("GROQ_API_KEY"),
        groq_model=os.getenv("GROQ_MODEL") or _streamlit_secret("GROQ_MODEL") or "openai/gpt-oss-20b",
    )
