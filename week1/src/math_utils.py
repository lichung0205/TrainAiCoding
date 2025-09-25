"""
math_utils.py - 數學工具模組
提供基本的數學運算函式
"""


def add(a, b):
    """
    加法運算
    參數:
        a: 第一個數字
        b: 第二個數字
    返回:
        兩數之和
    """
    return a + b


def subtract(a, b):
    """
    減法運算
    參數:
        a: 第一個數字
        b: 第二個數字
    返回:
        a 減去 b 的結果
    """
    return a - b


def multiply(a, b):
    """
    乘法運算
    參數:
        a: 第一個數字
        b: 第二個數字
    返回:
        兩數之積
    """
    return a * b


def divide(a, b):
    """
    除法運算
    參數:
        a: 被除數
        b: 除數
    返回:
        a 除以 b 的結果
    異常:
        ValueError: 當除數為 0 時拋出
    """
    if b == 0:
        raise ValueError("除數不能為零")
    return a / b


def power(base, exponent):
    """
    冪運算（額外功能）
    參數:
        base: 底數
        exponent: 指數
    返回:
        base 的 exponent 次方
    """
    return base**exponent


def is_even(number):
    """
    檢查數字是否為偶數（額外功能）
    參數:
        number: 要檢查的數字
    返回:
        True 如果數字是偶數，否則 False
    """
    return number % 2 == 0


# 測試程式碼（當直接執行此檔案時運行）
if __name__ == "__main__":
    # 測試所有函式
    print("測試 math_utils 模組:")
    print(f"5 + 3 = {add(5, 3)}")
    print(f"10 - 4 = {subtract(10, 4)}")
    print(f"6 * 7 = {multiply(6, 7)}")
    print(f"15 / 3 = {divide(15, 3)}")
    print(f"2^8 = {power(2, 8)}")
    print(f"16 是偶數嗎? {is_even(16)}")

    # 測試錯誤處理
    try:
        divide(10, 0)
    except ValueError as e:
        print(f"錯誤測試: {e}")
