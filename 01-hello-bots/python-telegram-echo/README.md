# Python Telegram Echo Bot

## 需求
- Python 3.11
- requests
- python-telegram-bot

## 目標
建立一個最小的 Telegram 回聲機器人，支援以下指令：
- `/start`
- `/ping` → 回覆 `pong`

## 執行步驟
```bash

## 有時候 Python 安裝時沒勾 pip，可以這樣補，這樣就能使用 pip 指令了
python -m ensurepip --upgrade

## 查看自己的版本
python --version
python -m pip --version


🚀 Python Telegram Echo Bot 快速啟動流程
1. 切到專案根目錄
cd D:\Dev\TrainAiCoding

2. 啟用虛擬環境
.venv\Scripts\Activate.ps1


👉 成功的話，你會看到提示字變成這樣：

(.venv) PS D:\Dev\TrainAiCoding>

3. 進入 Python 子專案資料夾
cd 01-hello-bots\python-telegram-echo

4. 安裝需求套件
python -m pip install -r requirements.txt python-dotenv

5. 建立 .env 檔案

在 python-telegram-echo/ 底下新建 .env，內容如下（把 token 換成你在 BotFather 建立 bot 時拿到的）：

TELEGRAM_BOT_TOKEN=123456789:ABC-your-bot-token

6. 執行 bot
python main.py

7. 測試

在 Telegram 跟你的 bot 對話：

輸入 /start → bot 應該會回「Hello! I'm your echo bot.」

輸入 /ping → bot 應該會回「pong」



## 測試方式
啟動後在 Telegram 對話框輸入：
- `/start` → 顯示歡迎訊息
- `/ping` → 回覆 `pong`
- `/help` → 顯示支援的指令清單
