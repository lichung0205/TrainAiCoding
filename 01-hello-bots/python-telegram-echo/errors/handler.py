"""
集中錯誤處理器
負責捕獲、處理和格式化所有錯誤
"""

import logging
import sys
from typing import Callable, Any
from functools import wraps

from .exceptions import (
    BaseAppError,
    UserInputError,
    DomainRuleError,
    SystemError,
    ERROR_EXIT_CODES,
)

logger = logging.getLogger(__name__)


class ErrorHandler:
    """全域錯誤處理器"""

    @staticmethod
    def handle_error(error: Exception) -> tuple[int, str]:
        """
        處理錯誤並返回退出碼和使用者訊息

        Args:
            error: 捕獲的異常

        Returns:
            tuple[int, str]: (退出碼, 使用者訊息)
        """
        # 如果是我們定義的應用程式錯誤
        if isinstance(error, BaseAppError):
            exit_code = ERROR_EXIT_CODES.get(type(error), 1)
            error_response = error.to_error_response()
            user_message = error_response.to_user_message()

            # 記錄結構化日誌
            logger.error(
                "Application error occurred",
                extra={
                    "error_code": error_response.code,
                    "correlation_id": error_response.correlation_id,
                    "error_type": type(error).__name__,
                },
            )

            return exit_code, user_message

        # 處理未預期的系統錯誤
        else:
            err_type = type(error).__name__
            system_error = SystemError(
                message=f"未預期的系統錯誤 ({err_type}): {str(error)}",
                hint="這可能是程式錯誤，請聯繫開發人員",
            )
            error_response = system_error.to_error_response()
            user_message = error_response.to_user_message()

            logger.error(
                "Unexpected system error",
                exc_info=True,
                extra={
                    "correlation_id": error_response.correlation_id,
                    "original_error": str(error),
                    "original_error_type": err_type,  # 可選
                },
            )
            return 1, user_message

    @staticmethod
    def telegram_error_wrapper(func: Callable) -> Callable:
        """
        Telegram Bot 錯誤處理裝飾器
        捕獲錯誤但不中斷 Bot 運行
        """

        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except BaseAppError as e:
                # 應用程式錯誤：回應使用者但繼續運行
                error_response = e.to_error_response()
                user_message = error_response.to_user_message()

                # 取得 update 物件來回覆訊息
                update = args[0] if args else None
                if update and hasattr(update, "message"):
                    await update.message.reply_text(user_message)

                logger.warning(
                    f"Bot command error: {e.message}",
                    extra={
                        "error_code": error_response.code,
                        "correlation_id": error_response.correlation_id,
                    },
                )
            except Exception as e:
                # 系統錯誤：記錄並回應通用錯誤訊息
                system_error = SystemError()
                error_response = system_error.to_error_response()
                user_message = error_response.to_user_message()

                update = args[0] if args else None
                if update and hasattr(update, "message"):
                    await update.message.reply_text(user_message)

                logger.error(
                    "Unexpected bot error",
                    exc_info=True,
                    extra={"correlation_id": error_response.correlation_id},
                )

        return wrapper


def main_error_handler(func: Callable) -> Callable:
    """
    Main 函數錯誤處理裝飾器
    捕獲所有錯誤並以適當的退出碼結束程式
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print("\n⚠️  程式被使用者中斷")
            sys.exit(130)  # 標準中斷退出碼
        except Exception as e:
            exit_code, user_message = ErrorHandler.handle_error(e)
            print(user_message)
            sys.exit(exit_code)

    return wrapper
