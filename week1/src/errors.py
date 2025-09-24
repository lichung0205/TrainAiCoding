class UserInputError(Exception):
    """使用者輸入錯誤例外類別"""

    pass


class DomainRuleError(Exception):
    """領域規則錯誤例外類別"""

    pass


class SystemError(Exception):
    """系統錯誤例外類別"""

    pass


def handle_error(exc):
    """
    處理錯誤並回傳對應的錯誤訊息

    Args:
        exc: 例外物件

    Returns:
        str: 錯誤處理結果訊息
    """
    if isinstance(exc, UserInputError):
        return "使用者輸入錯誤，請檢查輸入內容"
    elif isinstance(exc, DomainRuleError):
        return "違反業務規則，請確認操作是否符合規範"
    elif isinstance(exc, SystemError):
        return "系統發生錯誤，請聯繫管理員"
    else:
        return f"未知錯誤類型: {type(exc).__name__}"
