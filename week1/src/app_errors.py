# week1/src/app_errors.py
from __future__ import annotations


class AppError(Exception):
    """基底應用層錯誤（可帶 error_code 供上層映射 HTTP/退出碼）。"""

    error_code = "APP_ERROR"

    def __init__(self, message: str = "", *, detail: dict | None = None):
        super().__init__(message)
        self.detail = detail or {}


class UserInputError(AppError):
    error_code = "USER_INPUT_ERROR"


class DomainRuleError(AppError):
    error_code = "DOMAIN_RULE_ERROR"


class SystemError(AppError):
    error_code = "SYSTEM_ERROR"


def map_error(e: Exception) -> tuple[str, str]:
    """
    把 Exception 映射成 (error_code, friendly_message)。
    你未來可在這裡擴充映射規則。
    """
    if isinstance(e, AppError):
        return e.error_code, str(e) or e.__class__.__name__
    return "UNEXPECTED", f"未預期錯誤：{e!s}"
