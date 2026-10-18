# briefbot

A small research agent that runs entirely on your machine. Give it a topic: it searches the web,
reads the best pages, and writes a short brief with sources. Open source, no API keys.

It is a compact reference for the whole agent stack: LangGraph loop, tools, local model (Ollama),
prompt-injection-aware prompt, step limit, SSRF guard, structured logs, streaming API, tests, Docker, CI.

## Quick start

```powershell
ollama pull qwen2.5:7b
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements-dev.txt
.\.venv\Scripts\python -m briefbot.cli "how do vector databases work"
```

Pick another model with `$env:MODEL = "llama3.2"`.

## HTTP API (streams server-sent events)

```powershell
.\.venv\Scripts\python -m uvicorn briefbot.api:app --port 8000
curl.exe -N "http://127.0.0.1:8000/brief?topic=vector+databases"
```

## Tests

```powershell
.\.venv\Scripts\python -m pytest -q
```

Tests cover the tools and API without a model or network.

## Docker

```powershell
docker build -t briefbot .
docker run -p 8000:8000 briefbot
```

The container talks to Ollama on the host (`host.docker.internal:11434`).

## Safety notes

- `fetch_page` only fetches public http(s) URLs (blocks localhost and private ranges).
- The system prompt tells the model to treat page text as data, not instructions.
- The agent stops after a fixed number of steps.
- Small local models make mistakes. Check the cited sources before relying on a brief.

## Layout

| Path | What it is |
|---|---|
| `briefbot/tools.py` | `web_search`, `fetch_page` |
| `briefbot/agent.py` | the LangGraph loop |
| `briefbot/cli.py` | command line entry |
| `briefbot/api.py` | FastAPI + SSE streaming |
| `tests/` | pytest suite |