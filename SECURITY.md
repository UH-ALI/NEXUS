# Security and Data Handling

- Keep the Groq API key in `.streamlit/secrets.toml` locally or the host's secret manager. Never commit it or put it in screenshots/video.
- `.gitignore` excludes `.streamlit/secrets.toml`, `.venv/`, Python bytecode, and caches. Commit `.streamlit/secrets.toml.example`, which contains placeholders only.
- Uploaded content is processed in memory for text extraction. NEXUS does not persist uploads or provide filesystem/shell execution tools to the model.
- Treat document text and generated tool output as untrusted data. The planner can select only registered tools.
- A quiz format check verifies structure only; it does not establish factual accuracy.
- If a key is exposed in Git history, revoke it at the provider and issue a replacement; deleting the current file alone does not remove it from history.
