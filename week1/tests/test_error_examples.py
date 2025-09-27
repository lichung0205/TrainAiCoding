# week1/tests/test_error_examples.py
import pytest
from src.app_errors import UserInputError, DomainRuleError, SystemError, map_error
from src.error_examples import parse_age, apply_discount, read_config


def test_parse_age_ok():
    assert parse_age("18") == 18


def test_parse_age_invalid():
    with pytest.raises(UserInputError):
        parse_age("abc")


def test_apply_discount_ok():
    assert apply_discount(100, "vip") == 80.0


def test_apply_discount_unknown_tier():
    with pytest.raises(DomainRuleError):
        apply_discount(100, "gold")


def test_read_config_missing(tmp_path):
    with pytest.raises(SystemError):
        read_config(tmp_path / "nope.json")


def test_map_error_codes():
    code, msg = map_error(UserInputError("輸入錯誤"))
    assert code == "USER_INPUT_ERROR" and "輸入錯誤" in msg
