# TrainAiCoding

用 AI 進行程式訓練的實作專案（每日一進度，一次專注一種語言）。  
本週語言：**Python**（W1）。

## 快速開始
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
pytest -q

# 專案結構
src/            # 程式碼（共享，不因天數複製）
tests/          # 測試（pytest）
docs/
  logs/         # 每日訓練日誌（W1D1, W1D2…）
README.md       # 入門指南與總覽
CONTRIBUTING.md # 協作規範（分支/Commit/PR）



#任務B 錯誤處理最小示例

本專案示範了如何在 Python 中建立自訂例外類別，並用 pytest 驗證。

### 使用方法

1. 執行程式碼（範例 `errors.py`）：

```python
from errors import UserInputError, handle_error

try:
    raise UserInputError("Invalid input")
except Exception as e:
    print(handle_error(e))   # 輸出：USER_INPUT_ERROR

