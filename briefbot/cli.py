"""Command line: python -m briefbot.cli "topic" """
from __future__ import annotations

import sys
import time

import structlog

from .agent import run_brief

structlog.configure(processors=[structlog.processors.TimeStamper(fmt="iso"), structlog.processors.JSONRenderer()])
log = structlog.get_logger()


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if not args:
        print('Usage: python -m briefbot.cli "topic to research"')
        return 2
    topic = " ".join(args)
    start = time.perf_counter()
    answer = run_brief(topic)
    log.info("brief_done", topic=topic, seconds=round(time.perf_counter() - start, 1), chars=len(answer))
    print(answer)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())