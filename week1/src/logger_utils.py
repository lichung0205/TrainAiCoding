# logger_utils.py
from __future__ import annotations
import json
import logging
from logging.handlers import RotatingFileHandler
from typing import Optional, Dict, Any
from datetime import datetime, timezone

_DEFAULT_FMT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
_DATEFMT = "%Y-%m-%d %H:%M:%S"

_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def get_logger(
    name: str,
    level: str = "INFO",
    log_file: Optional[str] = None,
    max_bytes: int = 1_000_000,
    backup_count: int = 3,
) -> logging.Logger:
    """
    建立標準 Logger（console + optional rotating file）。
    """
    logger = logging.getLogger(name)
    logger.setLevel(_LEVELS.get(level.upper(), logging.INFO))
    logger.propagate = False  # 避免重複輸出

    # 若重複呼叫，先清空舊 handler
    if logger.handlers:
        logger.handlers.clear()

    fmt = logging.Formatter(_DEFAULT_FMT, datefmt=_DATEFMT)

    # Console
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    # File (rotating)
    if log_file:
        fh = RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
        )
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    return logger


def _now_iso_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def log_event(event: str, payload: Dict[str, Any], file_path: str) -> None:
    """
    以 JSON Lines 方式寫入事件（每行一筆），方便後續用工具掃描/彙整。
    """
    record = {
        "ts": _now_iso_utc(),
        "event": event,
        "payload": payload,
    }
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
