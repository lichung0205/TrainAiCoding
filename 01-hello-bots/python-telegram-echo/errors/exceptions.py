"""
錯誤類型定義模組
定義三種主要錯誤類型及統一錯誤格式
"""

import uuid
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class ErrorResponse:
    """統一錯誤回應格式"""

    code: str
    message: str
    hint: str
    correlation_id: str

    def to_dict(self) -> Dict[str, Any]:
        """轉換為字典格式"""
        return {
            "code": self.code,
            "message": self.message,
            "hint": self.hint,
            "correlationId": self.correlation_id,
        }

    def to_user_message(self) -> str:
        """轉換為使用者友善訊息格式"""
        return f"❌ {self.message}\n💡 {self.hint}\n🔍 追蹤ID: {self.correlation_id}"


class BaseAppError(Exception):
    """應用程式錯誤基底類別"""

    def __init__(
        self, message: str, hint: str = "", correlation_id: Optional[str] = None
    ):
        super().__init__(message)
        self.message = message
        self.hint = hint or "請聯繫系統管理員"
        self.correlation_id = correlation_id or str(uuid.uuid4())[:8]

    def to_error_response(self) -> ErrorResponse:
        """轉換為標準錯誤回應"""
        return ErrorResponse(
            code=self.__class__.__name__.replace("Error", "").upper(),
            message=self.message,
            hint=self.hint,
            correlation_id=self.correlation_id,
        )


class UserInputError(BaseAppError):
    """使用者輸入錯誤"""

    def __init__(
        self, message: str = "輸入參數錯誤", hint: str = "請檢查命令格式和參數"
    ):
        super().__init__(message, hint)


class DomainRuleError(BaseAppError):
    """業務規則違反錯誤"""

    def __init__(
        self, message: str = "業務規則違反", hint: str = "請確認操作符合業務邏輯"
    ):
        super().__init__(message, hint)


class SystemError(BaseAppError):
    """系統錯誤"""

    def __init__(
        self, message: str = "系統發生未預期錯誤", hint: str = "請稍後再試或聯繫管理員"
    ):
        super().__init__(message, hint)


# 錯誤代碼映射
ERROR_EXIT_CODES = {
    UserInputError: 2,
    DomainRuleError: 3,
    SystemError: 1,
    BaseAppError: 1,  # 兜底
}
