from __future__ import annotations
import json
import logging
import os
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
    # 環境變數控制等級
    env_level = os.getenv("LOG_LEVEL", "").upper()
    if env_level in _LEVELS:
        level = env_level
        print(f"使用環境變數 LOG_LEVEL={env_level}")

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


def log_event(
    event: str,
    payload: Dict[str, Any],
    file_path: str,
    version: str = "1.0.0",
    source: str = "tofu-hunter",
) -> None:
    """
    以 JSON Lines 方式寫入事件（每行一筆），方便後續用工具掃描/彙整。
    """
    record = {
        "ts": _now_iso_utc(),
        "version": version,
        "source": source,
        "event": event,
        "payload": payload,
    }
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


# 旋轉日誌驗證函數
def test_rotating_log():
    """測試日誌旋轉功能"""
    logger = get_logger(
        "rotating_test",
        log_file="rotate.log",
        max_bytes=200,  # 每 200 bytes 就旋轉
        backup_count=2,  # 保留 2 個備份文件
    )

    print("開始寫入 50 行日誌到 rotate.log...")
    for i in range(50):
        logger.info(f"這是第 {i+1} 行日誌訊息，用來測試日誌旋轉功能")

    print("日誌寫入完成，檢查 rotate.log, rotate.log.1, rotate.log.2 文件")


def test_env_level():
    """測試環境變數控制日誌等級"""

    # 測試 1: 沒有環境變數
    print("=== 測試 1: 沒有環境變數 ===")
    if "LOG_LEVEL" in os.environ:
        del os.environ["LOG_LEVEL"]

    logger1 = get_logger("test1")
    logger1.debug("這條 DEBUG 訊息應該不會顯示")
    logger1.info("這條 INFO 訊息會顯示")

    # 測試 2: 設置環境變數
    print("\n=== 測試 2: 設置 LOG_LEVEL=DEBUG ===")
    os.environ["LOG_LEVEL"] = "DEBUG"

    logger2 = get_logger("test2")
    logger2.debug("這條 DEBUG 訊息現在應該顯示")
    logger2.info("這條 INFO 訊息也會顯示")


def test_event_log():
    """測試事件日誌功能"""

    # 測試默認參數
    print("寫入事件日誌到 events.log...")

    # 事件 1: 使用默認 source 和 version
    log_event("user_login", {"user_id": 123, "status": "success"}, "events.log")

    # 事件 2: 自定義 source 和 version
    log_event(
        "data_processed",
        {"records": 100, "duration_ms": 250},
        "events.log",
        version="2.1.0",
        source="data-pipeline",
    )

    # 事件 3: 錯誤事件
    log_event(
        "error_occurred",
        {"error_code": "E1001", "message": "數據庫連接失敗"},
        "events.log",
        source="tofu-hunter",
    )

    print("事件日誌寫入完成，檢查 events.log 文件內容")


if __name__ == "__main__":
    # 測試旋轉日誌
    test_rotating_log()
    # 測試環境變數
    test_env_level()
    # 測試事件日誌
    test_event_log()
