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

## 需求套件
- 請以 requirements.txt 為準

pip install -r requirements.txt

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
python -m pip install -r requirements.txt

5. 建立 .env 檔案

在 python-telegram-echo/ 底下新建 .env，內容如下（把 token 換成你在 BotFather 建立 bot 時拿到的）：

TELEGRAM_BOT_TOKEN=123456789:ABC-your-bot-token

6. 執行 bot
python main.py

7. 測試

在 Telegram 跟你的 bot 對話：

輸入 /start → bot 應該會回「Hello! I'm your echo bot.」

輸入 /ping → bot 應該會回「Pong」

輸入 /time → bot 應該會回 台北時間：2025-09-23 16:54:38

輸入 /upper abcdefg → bot 應該會回 ABCDEFG


## 測試方式
啟動後在 Telegram 對話框輸入：
- `/start` → 顯示歡迎訊息
- `/ping` → 回覆 `Pong`
- `/help` → 顯示支援的指令清單
- `/time` → 回覆當下台北時間（格式：YYYY-MM-DD HH:MM:SS）。
- `/upper <文字>` → 把使用者輸入轉成全大寫回覆。


9/24 add
錯誤處理機制
錯誤類型分類
錯誤類型退出碼使用場景範例UserInputError2使用者輸入錯誤缺少參數、格式不正確DomainRuleError3業務規則違反文字過長、時區不支援SystemError1系統異常網路錯誤、IO 異常
錯誤訊息格式
所有錯誤都會以統一格式回應：
json{
  "code": "ERROR_CODE",
  "message": "人類可讀的錯誤描述",
  "hint": "解決方案建議",
  "correlationId": "唯一追蹤識別碼"
}
使用者會看到的格式：
❌ 錯誤描述
💡 解決建議
🔍 追蹤ID: abc12345
CLI 退出碼說明

0: 正常執行完畢
1: 系統錯誤（預設錯誤）
2: 使用者輸入錯誤
3: 業務規則錯誤
130: 使用者中斷（Ctrl+C）