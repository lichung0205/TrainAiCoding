"""
main.py - 示範如何使用 math_utils 模組
"""

# 方法 1: 導入整個模組
import math_utils

# 方法 2: 導入所有內容（不推薦，可能造成命名衝突）
# from math_utils import *


def demonstrate_math_utils():
    """示範 math_utils 模組的使用"""

    print("=== 數學工具模組使用示範 ===\n")

    # 使用 import math_utils 的方式
    print("1. 使用 import math_utils:")
    result1 = math_utils.add(10, 5)
    result2 = math_utils.subtract(20, 7)
    print(f"10 + 5 = {result1}")
    print(f"20 - 7 = {result2}")

    # 使用 from import 的方式
    result3 = math_utils.multiply(4, 6)
    print(f"4 × 6 = {result3}")

    # 使用所有功能
    print("3. 使用所有數學函式:")

    # 基本運算
    a, b = 25, 5
    print(f"{a} + {b} = {math_utils.add(a, b)}")
    print(f"{a} - {b} = {math_utils.subtract(a, b)}")
    print(f"{a} × {b} = {math_utils.multiply(a, b)}")
    print(f"{a} ÷ {b} = {math_utils.divide(a, b)}")

    # 進階功能
    print(f"\n4. 進階功能:")
    print(f"2的10次方 = {math_utils.power(2, 10)}")
    print(f"15是偶數嗎? {math_utils.is_even(15)}")

    # 錯誤處理示範
    print(f"\n5. 錯誤處理示範:")
    try:
        math_utils.divide(10, 0)
    except ValueError as e:
        print(f"錯誤捕獲: {e}")

    # 實際應用範例
    print(f"\n6. 實際應用範例:")

    # 檢查數字性質
    numbers = [12, 7, 24, 31, 8]
    print(f"\n數字檢查:")
    for num in numbers:
        even_status = "偶數" if math_utils.is_even(num) else "奇數"
        print(f"{num} 是 {even_status}")


def calculator_example():
    """簡單計算器範例"""
    print(f"\n=== 簡單計算器範例 ===")

    while True:
        print("\n選擇運算:")
        print("1. 加法")
        print("2. 減法")
        print("3. 乘法")
        print("4. 除法")
        print("5. 退出")

        choice = input("請輸入選擇 (1-5): ")

        if choice == "5":
            print("再見！")
            break

        if choice in ["1", "2", "3", "4"]:
            try:
                num1 = float(input("輸入第一個數字: "))
                num2 = float(input("輸入第二個數字: "))

                if choice == "1":
                    result = math_utils.add(num1, num2)
                    operator = "+"
                elif choice == "2":
                    result = math_utils.subtract(num1, num2)
                    operator = "-"
                elif choice == "3":
                    result = math_utils.multiply(num1, num2)
                    operator = "×"
                elif choice == "4":
                    result = math_utils.divide(num1, num2)
                    operator = "÷"

                print(f"結果: {num1} {operator} {num2} = {result}")

            except ValueError as e:
                print(f"輸入錯誤: {e}")
            except Exception as e:
                print(f"計算錯誤: {e}")
        else:
            print("無效選擇，請重新輸入")


if __name__ == "__main__":
    demonstrate_math_utils()
    calculator_example()
