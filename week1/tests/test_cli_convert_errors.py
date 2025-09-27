# week1/tests/test_cli_convert_errors.py
import sys
import subprocess
import shlex
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]  # 專案根目錄: .../TrainAiCoding
CLI_MOD = "week1.src.cli"


def run(cmd: str):
    # 直接組 list，避免把 sys.executable 與路徑丟進 shlex.split 造成 Windows 崩潰
    args = [sys.executable, "-m", CLI_MOD] + shlex.split(cmd)
    proc = subprocess.run(args, capture_output=True, text=True, cwd=ROOT)
    return proc.returncode, proc.stdout, proc.stderr


def test_convert_ok():
    code, out, err = run(
        'convert --dt "2025-09-26 10:00" --src-fmt "%Y-%m-%d %H:%M" --dst-fmt "%Y-%m-%d %H:%M" --src-tz Asia/Taipei --dst-tz UTC'
    )
    assert "轉換後時間：" in out and err == ""


def test_convert_invalid_tz():
    code, out, err = run(
        'convert --dt "2025-09-26 10:00" --src-fmt "%Y-%m-%d %H:%M" --dst-fmt "%Y-%m-%d %H:%M" --src-tz Nope/City --dst-tz UTC'
    )
    assert "錯誤：" in err and "時區" in err


def test_convert_invalid_format():
    code, out, err = run(
        'convert --dt "2025/09/26 10:00" --src-fmt "%Y-%m-%d %H:%M" --dst-fmt "%Y-%m-%d %H:%M" --src-tz Asia/Taipei --dst-tz UTC'
    )
    assert "錯誤：" in err and "格式不符" in err
