# time_utils.py
from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional, Union

try:
    # Python 3.9+
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    # 若你想強制用 pytz，也可自行改寫；這裡預設使用標準庫 zoneinfo
    raise

DatetimeLike = Union[datetime, str]


def _zone(tz: str) -> ZoneInfo:
    return ZoneInfo(tz)


def parse_dt(dt_str: str, fmt: str, tz: str) -> datetime:
    """
    將文字依格式解析成【有時區】datetime。
    """
    if not isinstance(dt_str, str):
        raise ValueError("dt_str must be a string")
    naive = datetime.strptime(dt_str, fmt)
    return naive.replace(tzinfo=_zone(tz))


def to_timezone(dt: datetime, tz: str) -> datetime:
    """
    將 aware datetime 轉換到指定時區。
    """
    if dt.tzinfo is None:
        raise ValueError("dt must be timezone-aware")
    return dt.astimezone(_zone(tz))


def format_dt(dt: datetime, fmt: str) -> str:
    """
    依格式輸出字串；若是 aware dt，可用 %Z/%z 取得時區資訊。
    """
    return dt.strftime(fmt)


def convert_format(
    dt_str: str, src_fmt: str, dst_fmt: str, src_tz: str, dst_tz: Optional[str] = None
) -> str:
    """
    將來源字串（含來源時區）轉為目標格式與時區；若未指定 dst_tz，沿用來源時區。
    """
    dt = parse_dt(dt_str, src_fmt, src_tz)
    if dst_tz:
        dt = to_timezone(dt, dst_tz)
    return format_dt(dt, dst_fmt)


def now_tz(tz: str) -> datetime:
    """
    取得指定時區的現在時間（aware）。
    """
    return datetime.now(timezone.utc).astimezone(_zone(tz))


def dt_to_unix(dt: datetime) -> float:
    """
    將 aware datetime 轉為 Unix timestamp（秒，含小數）。
    """
    if dt.tzinfo is None:
        raise ValueError("dt must be timezone-aware")
    return dt.timestamp()


def unix_to_dt(ts: float, tz: str) -> datetime:
    """
    將 Unix timestamp 轉回 aware datetime（指定時區）。
    """
    return datetime.fromtimestamp(ts, _zone(tz))
