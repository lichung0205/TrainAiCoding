"""
錯誤處理單元測試
驗證錯誤處理機制的正確性
"""

import pytest
import sys
from unittest.mock import Mock, patch, AsyncMock
import asyncio
from telegram import Update, Message, Chat, User

# 測試目標模組
from errors.exceptions import (
    UserInputError,
    DomainRuleError,
    SystemError,
    ErrorResponse,
    ERROR_EXIT_CODES,
)
from errors.handler import ErrorHandler, main_error_handler


class TestErrorExceptions:
    """測試錯誤類型定義"""

    def test_user_input_error_creation(self):
        """測試 UserInputError 建立與格式"""
        error = UserInputError("缺少參數", "請提供必要參數")
        response = error.to_error_response()

        assert response.code == "USERINPUT"
        assert response.message == "缺少參數"
        assert response.hint == "請提供必要參數"
        assert len(response.correlation_id) == 8

        user_msg = response.to_user_message()
        assert "❌ 缺少參數" in user_msg
        assert "💡 請提供必要參數" in user_msg

    def test_domain_rule_error_creation(self):
        """測試 DomainRuleError 建立與格式"""
        error = DomainRuleError("文字過長", "限制在100字內")
        response = error.to_error_response()

        assert response.code == "DOMAINRULE"
        assert response.message == "文字過長"
        assert response.hint == "限制在100字內"

    def test_system_error_creation(self):
        """測試 SystemError 建立與格式"""
        error = SystemError("資料庫連線失敗", "請聯繫管理員")
        response = error.to_error_response()

        assert response.code == "SYSTEM"
        assert response.message == "資料庫連線失敗"
        assert response.hint == "請聯繫管理員"


class TestErrorHandler:
    """測試錯誤處理器"""

    def test_handle_user_input_error(self):
        """測試處理使用者輸入錯誤"""
        error = UserInputError("參數錯誤")
        exit_code, message = ErrorHandler.handle_error(error)

        assert exit_code == ERROR_EXIT_CODES[UserInputError]  # 2
        assert "❌ 參數錯誤" in message
        assert "🔍 追蹤ID:" in message

    def test_handle_domain_rule_error(self):
        """測試處理業務規則錯誤"""
        error = DomainRuleError("業務邏輯違反")
        exit_code, message = ErrorHandler.handle_error(error)

        assert exit_code == ERROR_EXIT_CODES[DomainRuleError]  # 3
        assert "❌ 業務邏輯違反" in message

    def test_handle_system_error(self):
        """測試處理系統錯誤"""
        error = SystemError("未知錯誤")
        exit_code, message = ErrorHandler.handle_error(error)

        assert exit_code == ERROR_EXIT_CODES[SystemError]  # 1
        assert "❌ 未知錯誤" in message

    def test_handle_unexpected_error(self):
        """測試處理未預期的系統錯誤"""
        error = ValueError("意外的值錯誤")
        exit_code, message = ErrorHandler.handle_error(error)

        print(exit_code, message)

        assert exit_code == 1  # SystemError 的退出碼
        assert "❌ 未預期的系統錯誤" in message
        assert "ValueError" in message


class TestMainErrorHandler:
    """測試 main 函數錯誤處理裝飾器"""

    def test_successful_execution(self):
        """測試正常執行情況"""

        @main_error_handler
        def successful_main():
            return "success"

        result = successful_main()
        assert result == "success"

    def test_user_input_error_exit_code(self):
        """測試使用者輸入錯誤的退出碼"""

        @main_error_handler
        def failing_main():
            raise UserInputError("測試用戶錯誤")

        with patch("sys.exit") as mock_exit:
            with patch("builtins.print") as mock_print:
                failing_main()
                mock_exit.assert_called_once_with(2)
                mock_print.assert_called_once()
                printed_message = mock_print.call_args[0][0]
                assert "❌ 測試用戶錯誤" in printed_message

    def test_domain_rule_error_exit_code(self):
        """測試業務規則錯誤的退出碼"""

        @main_error_handler
        def failing_main():
            raise DomainRuleError("測試業務錯誤")

        with patch("sys.exit") as mock_exit:
            with patch("builtins.print") as mock_print:
                failing_main()
                mock_exit.assert_called_once_with(3)

    def test_system_error_exit_code(self):
        """測試系統錯誤的退出碼"""

        @main_error_handler
        def failing_main():
            raise SystemError("測試系統錯誤")

        with patch("sys.exit") as mock_exit:
            with patch("builtins.print") as mock_print:
                failing_main()
                mock_exit.assert_called_once_with(1)

    def test_unexpected_error_exit_code(self):
        """測試未預期錯誤的退出碼"""

        @main_error_handler
        def failing_main():
            raise RuntimeError("意外的運行錯誤")

        with patch("sys.exit") as mock_exit:
            with patch("builtins.print") as mock_print:
                failing_main()
                mock_exit.assert_called_once_with(1)  # SystemError 退出碼
                printed_message = mock_print.call_args[0][0]
                assert "RuntimeError" in printed_message

    def test_keyboard_interrupt_exit_code(self):
        """測試鍵盤中斷的退出碼"""

        @main_error_handler
        def interrupted_main():
            raise KeyboardInterrupt()

        with patch("sys.exit") as mock_exit:
            with patch("builtins.print") as mock_print:
                interrupted_main()
                mock_exit.assert_called_once_with(130)


class TestTelegramErrorWrapper:
    """測試 Telegram Bot 錯誤包裝器"""

    def setup_method(self):
        """設定測試環境"""
        # 建立 Mock Telegram 物件
        self.mock_user = Mock(spec=User)
        self.mock_chat = Mock(spec=Chat)
        self.mock_message = Mock(spec=Message)
        self.mock_update = Mock(spec=Update)

        # 這行要能被 await
        self.mock_message.reply_text = AsyncMock()
        self.mock_update.message = self.mock_message

    @pytest.mark.asyncio
    async def test_successful_telegram_command(self):
        """測試正常的 Telegram 指令執行"""

        @ErrorHandler.telegram_error_wrapper
        async def test_command(update, context):
            await update.message.reply_text("成功")
            return "success"

        result = await test_command(self.mock_update, None)
        assert result == "success"
        self.mock_message.reply_text.assert_called_with("成功")

    @pytest.mark.asyncio
    async def test_user_input_error_in_telegram(self):
        """測試 Telegram 指令中的使用者輸入錯誤"""

        @ErrorHandler.telegram_error_wrapper
        async def test_command(update, context):
            raise UserInputError("參數格式錯誤")

        await test_command(self.mock_update, None)

        # 驗證錯誤訊息被回覆給使用者
        self.mock_message.reply_text.assert_called_once()
        replied_message = self.mock_message.reply_text.call_args[0][0]
        assert "❌ 參數格式錯誤" in replied_message
        assert "🔍 追蹤ID:" in replied_message

    @pytest.mark.asyncio
    async def test_system_error_in_telegram(self):
        """測試 Telegram 指令中的系統錯誤"""

        @ErrorHandler.telegram_error_wrapper
        async def test_command(update, context):
            raise RuntimeError("意外錯誤")

        await test_command(self.mock_update, None)

        # 驗證系統錯誤被轉換為使用者友善訊息
        self.mock_message.reply_text.assert_called_once()
        replied_message = self.mock_message.reply_text.call_args[0][0]
        assert "❌ 系統發生未預期錯誤" in replied_message


# 整合測試
class TestIntegrationErrorFlow:
    """整合測試：完整錯誤處理流程"""

    def test_error_response_json_serialization(self):
        """測試錯誤回應的 JSON 序列化"""
        error = DomainRuleError("測試錯誤", "測試提示")
        response = error.to_error_response()
        json_data = response.to_dict()

        expected_keys = {"code", "message", "hint", "correlationId"}
        assert set(json_data.keys()) == expected_keys
        assert json_data["code"] == "DOMAINRULE"
        assert json_data["message"] == "測試錯誤"
        assert json_data["hint"] == "測試提示"

    def test_correlation_id_uniqueness(self):
        """測試關聯 ID 的唯一性"""
        error1 = UserInputError("錯誤1")
        error2 = UserInputError("錯誤2")

        id1 = error1.to_error_response().correlation_id
        id2 = error2.to_error_response().correlation_id

        assert id1 != id2
        assert len(id1) == 8
        assert len(id2) == 8


if __name__ == "__main__":
    # 執行測試
    pytest.main([__file__, "-v", "--tb=short"])
