from fastapi.testclient import TestClient

from briefbot import api


def test_health():
    assert TestClient(api.app).get("/health").json() == {"ok": True}


def test_brief_streams_events(monkeypatch):
    monkeypatch.setattr(api, "stream_brief", lambda topic: iter(["Hello ", "world"]))
    r = TestClient(api.app).get("/brief", params={"topic": "anything"})
    assert r.status_code == 200
    assert "data: Hello " in r.text and "event: done" in r.text


def test_brief_rejects_empty_topic():
    assert TestClient(api.app).get("/brief", params={"topic": ""}).status_code == 422