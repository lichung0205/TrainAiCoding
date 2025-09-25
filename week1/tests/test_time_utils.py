# tests/test_time_utils.py
import pytest
from datetime import datetime
from src.time_utils import (
    parse_dt,
    to_timezone,
    format_dt,
    convert_format,
    now_tz,
    dt_to_unix,
    unix_to_dt,
)

TPE = "Asia/Taipei"
UTC = "UTC"


def test_parse_dt_makes_aware():
    dt = parse_dt("2025-09-25 13:30", "%Y-%m-%d %H:%M", TPE)
    assert dt.tzinfo is not None
    assert format_dt(dt, "%Y-%m-%d %H:%M %Z") == "2025-09-25 13:30 CST"  # 台灣標準時間


def test_to_timezone_conversion():
    src = parse_dt("2025-09-25 13:30", "%Y-%m-%d %H:%M", TPE)
    utc_dt = to_timezone(src, UTC)
    # 台北 +08:00 => 同日 05:30 UTC
    assert format_dt(utc_dt, "%Y-%m-%d %H:%M %Z") == "2025-09-25 05:30 UTC"


def test_convert_format_end_to_end():
    out = convert_format(
        "25/09/2025 13:30",  # src string
        src_fmt="%d/%m/%Y %H:%M",
        dst_fmt="%Y-%m-%dT%H:%M:%S%z",
        src_tz=TPE,
        dst_tz=UTC,
    )
    assert out == "2025-09-25T05:30:00+0000"


def test_now_tz_is_aware():
    dt = now_tz(UTC)
    assert dt.tzinfo is not None
    assert format_dt(dt, "%Z") == "UTC"


def test_unix_roundtrip():
    dt = parse_dt("2025-09-25 00:00", "%Y-%m-%d %H:%M", UTC)
    ts = dt_to_unix(dt)
    back = unix_to_dt(ts, UTC)
    # 用到分鐘等級比對即可（避免秒小數誤差）
    assert format_dt(back, "%Y-%m-%d %H:%M") == "2025-09-25 00:00"


def test_invalid_timezone_raises():
    with pytest.raises(Exception):
        parse_dt("2025-01-01 00:00", "%Y-%m-%d %H:%M", "Not/AZone")


def test_invalid_input_raises():
    with pytest.raises(ValueError):
        parse_dt("bad-input", "%Y-%m-%d %H:%M", UTC)
