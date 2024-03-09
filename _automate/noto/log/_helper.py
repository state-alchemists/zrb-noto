import os
from datetime import datetime
from pathlib import Path

from _automate.noto._config import CURRENT_TIME, SRC_DIR


def get_log_file_name(current_time: datetime = CURRENT_TIME) -> str:
    year = current_time.year
    month = current_time.strftime("%m")
    date = current_time.strftime("%d")
    return os.path.join(
        SRC_DIR, "logs", f"{year}", f"{year}-{month}", f"{year}-{month}-{date}.md"
    )


def append_log(text: str, current_time: datetime = CURRENT_TIME) -> str:
    file_name = get_log_file_name(current_time=current_time)
    dir_path = Path(os.path.dirname(file_name))
    dir_path.mkdir(parents=True, exist_ok=True)
    time_str: str = current_time.strftime("%H:%M")
    with open(file_name, "a") as file:
        file.write(f"- {time_str}: {text}\n")


def get_log(file_name: str) -> str:
    dir_path = Path(os.path.dirname(file_name))
    dir_path.mkdir(parents=True, exist_ok=True)
    if not os.path.isfile(file_name):
        return ""
    with open(file_name, "r") as file:
        return file.read()
