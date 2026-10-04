# Deployment — Streamlit Community Cloud

## Before deployment

- Push the project root (the folder containing `app.py` and `requirements.txt`) to GitHub.
- Confirm `.streamlit/secrets.toml`, `.venv`, and `__pycache__` are absent from the commit.
- Ensure `requirements.txt` is at the repository root.

## Deploy

1. Sign in to Streamlit Community Cloud and connect the GitHub account that can access the repository.
2. Choose **Create app** and select the repository and branch.
3. Set the app entrypoint to `app.py` at the repository root.
4. In **Advanced settings / Secrets**, enter the same TOML values as the local secrets file:

   ```toml
   GROQ_API_KEY = "your-key"
   GROQ_MODEL = "openai/gpt-oss-20b"
   ```

5. Deploy and watch the build logs. Share the generated `*.streamlit.app` URL only after testing it in a private browser window.

Streamlit Community Cloud installs dependencies from `requirements.txt` and reads cloud secrets from the app settings. Never commit `.streamlit/secrets.toml`. See the official [deployment guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy), [dependency guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies), and [secrets guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management).

## Smoke check

- Open the deployed link while signed out.
- Run a no-upload goal and an upload-based study/quiz request.
- Check the run trace, validation message, output, and download.
- Confirm errors are understandable when a file cannot be read or the API key is absent.
