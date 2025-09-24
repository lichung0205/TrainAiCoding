import pytest
from src.errors import UserInputError, DomainRuleError, SystemError, handle_error


# 測試資料參數化
@pytest.mark.parametrize(
    "exception,expected_message",
    [
        # 測試三種自訂例外
        (UserInputError("無效輸入"), "使用者輸入錯誤，請檢查輸入內容"),
        (DomainRuleError("規則違反"), "違反業務規則，請確認操作是否符合規範"),
        (SystemError("系統故障"), "系統發生錯誤，請聯繫管理員"),
        # 測試未知例外
        (ValueError("非預期錯誤"), "未知錯誤類型: ValueError"),
        (TypeError("型別錯誤"), "未知錯誤類型: TypeError"),
    ],
)
def test_handle_error(exception, expected_message):
    """測試 handle_error 函數對不同例外的處理"""
    result = handle_error(exception)
    assert result == expected_message


def test_handle_error_with_custom_message():
    """測試帶有自訂訊息的例外處理"""
    custom_error = UserInputError("電子郵件格式錯誤")
    result = handle_error(custom_error)
    assert result == "使用者輸入錯誤，請檢查輸入內容"

    # 確認原始錯誤訊息仍然可用
    assert str(custom_error) == "電子郵件格式錯誤"


def test_exception_hierarchy():
    """測試例外繼承關係"""
    # 確認所有自訂例外都繼承自 Exception
    assert issubclass(UserInputError, Exception)
    assert issubclass(DomainRuleError, Exception)
    assert issubclass(SystemError, Exception)
