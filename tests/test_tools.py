from briefbot.tools import clean_html, is_safe_url, fetch_page


def test_clean_html_strips_tags_and_scripts():
    raw = "<html><script>alert(1)</script><style>p{}</style><p>Hello &amp; welcome</p></html>"
    assert clean_html(raw) == "Hello & welcome"


def test_safe_url_accepts_public_https():
    assert is_safe_url("https://example.com/page")


def test_safe_url_blocks_local_and_private():
    for bad in ["http://localhost:8000", "http://127.0.0.1/x", "http://192.168.1.5", "http://10.0.0.1",
                "file:///etc/passwd", "ftp://example.com", "http://service.internal/x"]:
        assert not is_safe_url(bad), bad


def test_fetch_page_refuses_unsafe_url_without_network():
    assert fetch_page.invoke({"url": "http://127.0.0.1/secret"}).startswith("Refused")