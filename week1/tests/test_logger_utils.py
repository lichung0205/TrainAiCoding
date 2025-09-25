# tests/test_logger_utils.py
from src.logger_utils import get_logger, log_event
from src.time_utils import parse_dt, format_dt
from pathlib import Path


def test_logger_writes_to_file(tmp_path):
    log_file = tmp_path / "app.log"
    logger = get_logger("day2b", level="INFO", log_file=str(log_file))

    logger.info("hello %s", "world")
    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    assert "hello world" in content


def test_log_event_jsonl(tmp_path):
    import json

    log_file = tmp_path / "events.jsonl"
    log_event("trade", {"side": "buy", "qty": 3}, file_path=str(log_file))
    log_event("trade", {"side": "sell", "qty": 2}, file_path=str(log_file))

    lines = log_file.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 2
    rec = json.loads(lines[0])
    assert rec["event"] == "trade"
    assert rec["payload"]["qty"] == 3
