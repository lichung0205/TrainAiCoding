import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from dotenv import load_dotenv

# 載入 .env 檔案
load_dotenv()

# 設定日誌
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """處理 /start 指令。"""
    await update.message.reply_text(
        "哈囉！我是一個簡單的 echo bot。請隨便傳送訊息給我！"
    )


async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """處理 /ping 指令。"""
    await update.message.reply_text("Pong!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """處理 /help 指令。"""
    await update.message.reply_text(
        "支援的指令：\n"
        "/start - 開始使用 bot\n"
        "/ping - 測試 bot 是否在線\n"
        "/help - 顯示本指令清單"
    )


async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """將使用者傳送的訊息原樣回傳。"""
    await update.message.reply_text(update.message.text)


def main() -> None:
    """啟動 bot。"""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("請在 .env 檔案中設定 TELEGRAM_BOT_TOKEN。")

    application = Application.builder().token(token).build()

    # 註冊指令處理器
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("ping", ping_command))
    application.add_handler(CommandHandler("help", help_command))  # 新增 /help 指令

    # 註冊訊息處理器，處理所有非指令的文字訊息
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message)
    )

    # 啟動 bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
