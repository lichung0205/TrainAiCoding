import argparse
import datetime
import json
import logging
from logging import handlers
import pytz
import sys
from pathlib import Path

from typing import Tuple
from .app_errors import UserInputError


# --- 在 convert_datetime 上方加入這個純函式 ---
def convert_core(
    dt: str, src_fmt: str, dst_fmt: str, src_tz: str, dst_tz: str
) -> Tuple[str, str]:
    """
    回傳 (原始aware字串, 轉換後格式化字串)；錯誤時丟出 UserInputError。
    """
    try:
        source_tz = pytz.timezone(src_tz)
        dest_tz = pytz.timezone(dst_tz)
    except pytz.UnknownTimeZoneError as e:
        raise UserInputError(f"無效的時區名稱：{e}") from e

    try:
        dt_naive = datetime.datetime.strptime(dt, src_fmt)
    except ValueError as e:
        raise UserInputError(f"日期時間或格式不符：{e}") from e

    dt_aware = source_tz.localize(dt_naive)
    dt_converted = dt_aware.astimezone(dest_tz)
    return dt_aware.isoformat(), dt_converted.strftime(dst_fmt)


# --- 將 convert_datetime 改成呼叫 convert_core（原本印出行為保留） ---
def convert_datetime(args):
    """處理 'convert' 子命令."""
    try:
        aware, formatted = convert_core(
            args.dt, args.src_fmt, args.dst_fmt, args.src_tz, args.dst_tz
        )
        print(f"原始時間：{aware}")
        print(f"轉換後時間：{formatted}")
    except UserInputError as e:
        print(f"錯誤：{e}", file=sys.stderr)
    except Exception as e:
        print(f"發生未預期的錯誤：{e}", file=sys.stderr)


def _setup_logger(
    level: str, file_path: str | None, rotate: bool, max_bytes: int, backup_count: int
) -> logging.Logger:
    logger = logging.getLogger("day3")
    logger.setLevel(getattr(logging, level))

    # 清掉舊 handler，避免重複輸出
    logger.handlers.clear()

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    sh.setLevel(getattr(logging, level))
    logger.addHandler(sh)

    # File (optional)
    if file_path:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        if rotate:
            fh = handlers.RotatingFileHandler(
                file_path,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding="utf-8",
            )
        else:
            fh = logging.FileHandler(file_path, encoding="utf-8")
        fh.setFormatter(fmt)
        fh.setLevel(getattr(logging, level))
        logger.addHandler(fh)

    return logger


def log_event(args):
    """處理 'log' 子命令：用 logging 輸出訊息（可寫檔）。"""
    logger = _setup_logger(
        level=args.level,
        file_path=args.file,
        rotate=args.rotate,
        max_bytes=args.max_bytes,
        backup_count=args.backup_count,
    )

    # 依等級輸出
    msg = args.message
    if args.level == "DEBUG":
        logger.debug(msg)
    elif args.level == "INFO":
        logger.info(msg)
    elif args.level == "WARNING":
        logger.warning(msg)
    elif args.level == "ERROR":
        logger.error(msg)
    else:
        logger.critical(msg)

    # 顯示寫檔位置（若有）
    if args.file:
        print(f"→ 已寫入：{args.file}")


def main():
    parser = argparse.ArgumentParser(
        description="一個多功能的 CLI 工具，用於時間轉換和日誌記錄。",
        epilog="使用 '<command> --help' 查看更多資訊。",
    )
    subparsers = parser.add_subparsers(dest="command", help="可用的子命令")

    # --- 'convert' 子命令 ---
    convert_parser = subparsers.add_parser("convert", help="轉換日期時間的格式和時區")
    convert_parser.add_argument("--dt", required=True, help="要轉換的日期時間字串")
    convert_parser.add_argument(
        "--src-fmt", required=True, help="原始格式 (e.g., '%Y-%m-%d %H:%M')"
    )
    convert_parser.add_argument(
        "--dst-fmt", required=True, help="目標格式 (e.g., '%Y-%m-%d %H:%M')"
    )
    convert_parser.add_argument(
        "--src-tz", default="Asia/Taipei", help="原始時區 (預設: Asia/Taipei)"
    )
    convert_parser.add_argument("--dst-tz", default="UTC", help="目標時區 (預設: UTC)")
    convert_parser.set_defaults(func=convert_datetime)

    # --- 'log' 子命令（改為設定 logging） ---
    log_parser = subparsers.add_parser("log", help="輸出一則 log（可同時寫檔）")
    log_parser.add_argument(
        "--level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="log 等級（預設: INFO）",
    )
    log_parser.add_argument(
        "--message", "-m", default="Hello from Day3 logging!", help="log 訊息內容"
    )
    log_parser.add_argument("--file", help="寫入的檔案路徑（若不提供則只輸出到主控台）")
    log_parser.add_argument(
        "--rotate",
        action="store_true",
        help="啟用 RotatingFileHandler（輪轉檔案）",
    )
    log_parser.add_argument(
        "--max-bytes",
        type=int,
        default=512_000,
        help="輪轉檔案大小上限（預設 512KB）",
    )
    log_parser.add_argument(
        "--backup-count",
        type=int,
        default=3,
        help="輪轉備份檔數量（預設 3）",
    )
    log_parser.set_defaults(func=log_event)

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    if hasattr(args, "func"):
        args.func(args)


if __name__ == "__main__":
    main()
