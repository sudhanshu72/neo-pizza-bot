# Neo Pizza Sagar AI Assistant

A small Streamlit + Groq chatbot that helps customers explore the menu of
**Neo Pizza Sagar** &mdash; the first wood-fired pizzeria in Sagar, MP. Built
to demonstrate domain-grounded LLM responses, light guardrails, and persistent
chat memory in a Streamlit UI.

## What it does

- Educates customers about wood-fired pizza vs standard baked pizza
  (temperature, oil content, dough fermentation).
- Answers menu questions from a curated knowledge base in the system prompt.
- Stays on-topic via prompt-level guardrails (politely declines off-topic
  questions like coding, politics, or other restaurants).
- Remembers the conversation within a session so customers can ask follow-ups.

## Tech stack

- **LLM**: Groq (Llama 3.1 8B Instant via `langchain-groq`)
- **UI / state**: Streamlit (`st.chat_input`, `st.chat_message`, session state)
- **Memory**: in-session message list with `SystemMessage` / `HumanMessage` /
  `AIMessage` from `langchain-core`

## Project layout

```
.
|-- app.py                  # Streamlit app + system prompt + chat loop
|-- requirements.txt
|-- .devcontainer/          # VS Code dev container config
`-- .gitignore
```

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate      # on Windows
pip install -r requirements.txt

# Provide your Groq key via Streamlit secrets or environment
mkdir -p .streamlit
echo 'GROQ_API_KEY = "your-key-here"' > .streamlit/secrets.toml

streamlit run app.py
```

## Notable design choices

- The full menu and "wood-fired story" live in a single `SYSTEM_PROMPT`
  constant. Easy to edit, no DB needed for a single-store assistant.
- Guardrails are prompt-level only &mdash; appropriate for a small, low-risk
  domain. For higher-stakes use cases (e.g. medical, financial), a separate
  classifier call would be safer.
- API key is read from `st.secrets` first (for Streamlit Cloud) and falls back
  to `os.getenv` (for local dev).

## License

MIT &mdash; small portfolio / demo project.
