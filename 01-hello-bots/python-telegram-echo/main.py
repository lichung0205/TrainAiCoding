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

# 新增：匯入錯誤處理模組
from errors.exceptions import UserInputError, DomainRuleError, SystemError
from errors.handler import ErrorHandler, main_error_handler

# 載入 .env 檔案
load_dotenv()

# 設定日誌
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


@ErrorHandler.telegram_error_wrapper
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """處理 /start 指令。"""
    await update.message.reply_text(
        "哈囉！我是一個簡單的 echo bot。請隨便傳送訊息給我！"
    )


@ErrorHandler.telegram_error_wrapper
async def time_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """處理 /time 指令。回覆當下台北時間（格式：YYYY-MM-DD HH:MM:SS）。"""
    from datetime import datetime
    import pytz

    try:
        taipei_tz = pytz.timezone("Asia/Taipei")
        taipei_time = datetime.now(taipei_tz)
        formatted_time = taipei_time.strftime("%Y-%m-%d %H:%M:%S")
        await update.message.reply_text(f"台北時間：{formatted_time}")
    except Exception as e:
        # 將系統錯誤包裝為我們的錯誤類型
        raise SystemError(
            message="無法取得時間資訊", hint="時區設定可能有問題，請稍後再試"
        ) from e


@ErrorHandler.telegram_error_wrapper
async def upper_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """處理 /upper 指令。把使用者輸入轉成全大寫回覆"""
    if not context.args:
        raise UserInputError(
            message="缺少要轉換的文字參數", hint="使用方式：/upper <要轉換的文字>"
        )

    text = " ".join(context.args)

    # 新增：業務規則驗證
    if len(text) > 200:
        raise DomainRuleError(
            message="文字長度超過限制", hint="單次轉換文字不能超過 200 個字符"
        )

    if not text.strip():
        raise UserInputError(
            message="不能轉換空白文字", hint="請提供有內容的文字進行轉換"
        )

    await update.message.reply_text(text.upper())


@ErrorHandler.telegram_error_wrapper
async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """處理 /ping 指令。"""
    await update.message.reply_text("Pong!")


@ErrorHandler.telegram_error_wrapper
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


@ErrorHandler.telegram_error_wrapper
async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """將使用者傳送的訊息原樣回傳。"""
    if not update.message.text:
        raise UserInputError(message="無法處理空訊息", hint="請傳送文字訊息給我")

    await update.message.reply_text(update.message.text)


# 新增：啟動時自動把指令清單註冊到 Telegram 選單
async def post_init(app: Application) -> None:
    """啟動時自動把指令清單註冊到 Telegram 選單"""
    try:
        await app.bot.set_my_commands(
            [
                BotCommand("start", "開始使用 bot"),
                BotCommand("ping", "測試 bot 是否在線"),
                BotCommand("help", "顯示指令清單"),
                BotCommand("time", "回覆台北時間"),
                BotCommand("upper", "把文字轉成全大寫"),
            ]
        )
    except Exception as e:
        raise SystemError(
            message="無法註冊 Bot 指令選單", hint="請檢查 Bot Token 是否正確或網路連線"
        ) from e


@main_error_handler
def main() -> None:
    """啟動 bot。"""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise UserInputError(
            message="缺少 Telegram Bot Token",
            hint="請在 .env 檔案中設定 TELEGRAM_BOT_TOKEN",
        )

    try:
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
        print("🤖 Bot 啟動中...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)

    except Exception as e:
        # 將任何啟動錯誤包裝為系統錯誤
        raise SystemError(
            message="Bot 啟動失敗", hint="請檢查網路連線和 Token 設定"
        ) from e


if __name__ == "__main__":
    main()
# --- IGNORE ---
