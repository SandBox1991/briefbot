"""HTTP service. Run:  python -m uvicorn briefbot.api:app --port 8000
Try:  curl -N "http://127.0.0.1:8000/brief?topic=vector+databases"
"""
from __future__ import annotations

from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse

from .agent import stream_brief

app = FastAPI(title="briefbot")


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/brief")
def brief(topic: str = Query(min_length=2, max_length=200)):
    def events():
        for text in stream_brief(topic):
            yield "data: " + text.replace("\n", "\\n") + "\n\n"
        yield "event: done\ndata: end\n\n"

    return StreamingResponse(events(), media_type="text/event-stream")