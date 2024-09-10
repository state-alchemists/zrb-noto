import os
import re
from datetime import datetime
from pathlib import Path

from zrb.helper.accessories.color import colored

from .._config import LOG_ABS_DIR_PATH

_STATUS_COLOR_MAP = {
    "START": "light_cyan",
    "COMPLETE": "light_green",
    "STOP": "light_yellow",
    "ADD": "cyan",
    "EDIT": "green",
    "DELETE": "yellow",
}


def get_log_file_name(current_time: datetime) -> str:
    year = current_time.year
    month = current_time.strftime("%m")
    date = current_time.strftime("%d")
    return os.path.join(
        LOG_ABS_DIR_PATH, f"{year}", f"{year}-{month}", f"{year}-{month}-{date}.md"
    )


def append_log_item(text: str, current_time: datetime) -> str:
    file_name = get_log_file_name(current_time=current_time)
    dir_path = Path(os.path.dirname(file_name))
    dir_path.mkdir(parents=True, exist_ok=True)
    time_str: str = current_time.strftime("%H:%M")
    log_lines = _get_log_lines(file_name)
    log_lines.append(f"- {time_str}: {text}\n")
    with open(file_name, "w") as file:
        file.write("\n".join(log_lines))
        file.write("\n")


def _get_log_lines(file_name: str) -> list[str]:
    log_str = get_log(file_name)
    return log_str.split("\n")


def get_pretty_log_lines(file_name: str) -> list[str]:
    log_str = get_log(file_name)
    for keyword, color in _STATUS_COLOR_MAP.items():
        log_str = re.sub(
            re.compile("([\n]*- \\d{2}:\\d{2}): __" + keyword + "__"),
            lambda match: match.group(1) + ": " + colored(keyword, color=color),
            log_str,
        )
    log_str = re.sub(
        r"__(.*?)__", lambda match: colored(match.group(1), color="yellow"), log_str
    )
    return log_str.split("\n")


def get_log(file_name: str) -> str:
    dir_path = Path(os.path.dirname(file_name))
    dir_path.mkdir(parents=True, exist_ok=True)
    if not os.path.isfile(file_name):
        return ""
    with open(file_name, "r") as file:
        return file.read().strip()
