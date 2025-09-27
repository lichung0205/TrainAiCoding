# week1/src/error_examples.py
from __future__ import annotations
from pathlib import Path
from .app_errors import UserInputError, DomainRuleError, SystemError


def parse_age(text: str) -> int:
    """示範：把年齡字串轉 int；錯誤回報 UserInputError。"""
    text = (text or "").strip()
    if not text.isdigit():
        raise UserInputError("年齡必須是正整數字串")
    age = int(text)
    if age <= 0:
        raise UserInputError("年齡必須 > 0")
    return age


def apply_discount(price: float, tier: str) -> float:
    """示範：商業規則錯誤（DomainRuleError）。"""
    if price < 0:
        raise UserInputError("價格不能為負數")
    tiers = {"vip": 0.8, "pro": 0.9, "normal": 1.0}
    if tier not in tiers:
        raise DomainRuleError(f"未知的會員等級：{tier}")
    return round(price * tiers[tier], 2)


def read_config(path: str) -> str:
    """示範：系統/IO 錯誤（SystemError）。"""
    p = Path(path)
    if not p.exists():
        raise SystemError(f"設定檔不存在：{path}")
    try:
        return p.read_text(encoding="utf-8")
    except OSError as e:
        raise SystemError(f"讀取設定檔失敗：{e}") from e
