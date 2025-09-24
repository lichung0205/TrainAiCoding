## CONTRIBUTING.md
# 專案協作規範文件
感謝您對專案的貢獻！為確保團隊協作順暢，請遵循以下規範：

1.  **分支命名**：
    `feature/`、`fix/`、`docs/`、`refactor/` + 簡短說明，例如 `feature/add-user-login`。
2.  **Commit 訊息**：
    `[Type]` `[Description]`，例如 `feat: 新增使用者登入功能`。
    - `feat`: 新功能
    - `fix`: 錯誤修復
    - `docs`: 文件更動
    - `style`: 程式碼格式調整
    - `refactor`: 重構
    - `test`: 測試相關
    - `chore`: 其他雜項更動
3.  **PR 驗收**：
    - 至少一位成員審核（Approve）。
    - 必須通過 CI/CD 流程。
    - 說明 PR 目的、內容與相關問題編號。
    - 確保所有測試案例都已通過。
    - 保持程式碼整潔，避免不必要的註解或變動。

---

### Gemini CLI 指令速記

* `gcloud auth application-default login`：登入 Google Cloud 帳戶並設定應用程式預設憑證。
* `gemini models list`：列出所有可用的 Gemini 模型。
* `gemini chat --model=gemini-1.5-pro`：與指定模型進行互動式聊天。