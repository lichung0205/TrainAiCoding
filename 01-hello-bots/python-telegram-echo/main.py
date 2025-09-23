import os
import logging
from telegram import Update, BotCommand
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


# /time 指令。回覆當下台北時間（格式：YYYY-MM-DD HH:MM:SS）。
async def time_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """處理 /time 指令。"""
    from datetime import datetime
    import pytz

    taipei_tz = pytz.timezone("Asia/Taipei")
    taipei_time = datetime.now(taipei_tz)
    formatted_time = taipei_time.strftime("%Y-%m-%d %H:%M:%S")
    await update.message.reply_text(f"台北時間：{formatted_time}")


# /upper <文字> → 把使用者輸入轉成全大寫回覆
async def upper_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """處理 /upper 指令。"""
    if context.args:
        text = " ".join(context.args)
        await update.message.reply_text(text.upper())
    else:
        await update.message.reply_text("請提供要轉換的文字。")


async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """處理 /ping 指令。"""
    await update.message.reply_text("Pong!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """處理 /help 指令。"""
    await update.message.reply_text(
        "支援的指令：\n"
        "/start - 開始使用 bot\n"
        "/ping - 測試 bot 是否在線\n"
        "/help - 顯示本指令清單\n"
        "/time - 回覆當下台北時間（格式：YYYY-MM-DD HH:MM:SS）\n"
        "/upper <文字> - 把使用者輸入轉成全大寫回覆"
    )


async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """將使用者傳送的訊息原樣回傳。"""
    await update.message.reply_text(update.message.text)


# 新增：啟動時自動把指令清單註冊到 Telegram 選單
async def post_init(app: Application) -> None:
    await app.bot.set_my_commands(
        [
            BotCommand("start", "開始使用 bot"),
            BotCommand("ping", "測試 bot 是否在線"),
            BotCommand("help", "顯示指令清單"),
            BotCommand("time", "回覆台北時間"),
            BotCommand("upper", "把文字轉成全大寫"),
        ]
    )


def main() -> None:
    """啟動 bot。"""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("請在 .env 檔案中設定 TELEGRAM_BOT_TOKEN。")

    # 加入 post_init
    application = Application.builder().token(token).post_init(post_init).build()

    # 註冊指令處理器
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("ping", ping_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("time", time_command))
    application.add_handler(CommandHandler("upper", upper_command))

    # 註冊訊息處理器，處理所有非指令的文字訊息
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message)
    )

    # 啟動 bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
# --- IGNORE ---
