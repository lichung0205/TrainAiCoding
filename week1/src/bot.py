# bot.py
import asyncio
import logging
from logging import handlers
from pathlib import Path
import os
import time
import shlex
import argparse

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv


# ===== Logging setup (console + rotating file) =====
def setup_logging(
    level="INFO",
    file_path="logs/bot.log",
    rotate=True,
    max_bytes=1_048_576,
    backup_count=5,
):
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, level))
    logger.handlers.clear()

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    sh.setLevel(getattr(logging, level))
    logger.addHandler(sh)

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

    # 降噪：將 http/telegram 套件 log 降到 WARNING
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("telegram").setLevel(logging.WARNING)


# ===== Decorator: auto log every command =====
def log_command(handler_name: str):
    def deco(func):
        async def wrapper(
            update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs
        ):
            user = update.effective_user
            chat = update.effective_chat
            text = update.effective_message.text if update.effective_message else ""
            start = time.perf_counter()
            logging.info(
                f"[CALL] {handler_name} | user={user.id if user else None} "
                f"(@{user.username if user else ''}) | chat={chat.id if chat else None} | text={text}"
            )
            try:
                result = await func(update, context, *args, **kwargs)
                ok = True
                return result
            except Exception as e:
                ok = False
                logging.exception(f"[ERROR] {handler_name} failed: {e}")
                # 讓使用者也知道失敗（不中斷程式）
                if update.effective_message:
                    await update.effective_message.reply_text(f"指令處理失敗：{e}")
            finally:
                cost = (time.perf_counter() - start) * 1000
                logging.info(f"[DONE] {handler_name} | ok={ok} | latency_ms={cost:.1f}")

        return wrapper

    return deco


# ===== convert 參數解析器（與 CLI 一致） =====
def build_convert_parser():
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("--dt", required=True)
    p.add_argument("--src-fmt", required=True)
    p.add_argument("--dst-fmt", required=True)
    p.add_argument("--src-tz", default="Asia/Taipei")
    p.add_argument("--dst-tz", default="UTC")
    return p


# ===== 導入你現有的 convert 邏輯 =====
# 我們直接重用你在 week1/src/cli.py 裡的 convert_datetime 函式
# （它吃 argparse.Namespace）
import sys
from types import SimpleNamespace

sys.path.append("week1/src")
from cli import convert_datetime  # noqa: E402


# ===== Handlers =====
@log_command("start")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "嗨～我是 Day3 Bot！\n"
        "可用指令：\n"
        '/convert --dt "2025-09-26 10:00" --src-fmt "%Y-%m-%d %H:%M" --dst-fmt "%Y-%m-%d %H:%M" --src-tz Asia/Taipei --dst-tz UTC\n'
        "/help 取得說明"
    )


@log_command("help")
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "指令說明：\n"
        "• /convert 進行時區與格式轉換（參數同 CLI）。\n"
        "  範例：\n"
        '  /convert --dt "2025-09-26 10:00" --src-fmt "%Y-%m-%d %H:%M" --dst-fmt "%Y-%m-%d %H:%M" --src-tz Asia/Taipei --dst-tz UTC\n'
    )


@log_command("convert")
async def convert_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return await update.message.reply_text("沒有讀到指令文字。")

    # 取出 /convert 後面的參數字串
    raw = update.message.text
    # 去掉前綴 "/convert"
    arg_str = raw.split(" ", 1)[1] if " " in raw else ""

    # 用 shlex 按 shell 規則切（支援引號）
    tokens = shlex.split(arg_str)
    parser = build_convert_parser()
    try:
        args = parser.parse_args(tokens)
    except SystemExit:
        return await update.message.reply_text(
            "參數錯誤。用法：/convert --dt ... --src-fmt ... --dst-fmt ... [--src-tz ...] [--dst-tz ...]"
        )

    # call 你的 convert_datetime；它會直接 print 結果到 stdout
    # 我們包一層，把結果彙整回 Telegram
    from io import StringIO
    import contextlib

    buf = StringIO()
    with contextlib.redirect_stdout(buf):
        convert_datetime(
            SimpleNamespace(
                dt=args.dt,
                src_fmt=args.__dict__["src_fmt"],
                dst_fmt=args.__dict__["dst_fmt"],
                src_tz=args.__dict__["src_tz"],
                dst_tz=args.__dict__["dst_tz"],
            )
        )
    output = buf.getvalue().strip() or "（無輸出）"
    await update.message.reply_text(f"執行結果：\n{output}")


# ===== main =====
# --- 取代檔尾整段 ---
def main():
    load_dotenv()
    setup_logging(level=os.getenv("LOG_LEVEL", "INFO"))

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("請在 .env 內設定 TELEGRAM_BOT_TOKEN=xxxxx")

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("convert", convert_cmd))

    logging.info("Bot started.")
    # 這行會自動 initialize / start / polling / idle / stop
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
