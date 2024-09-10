import datetime
import os
from collections.abc import Mapping
from typing import Any

from zrb import MultilineInput, StrInput

from .._config import CURRENT_TIME
from ._helper import get_log_file_name


def _get_default_content(input_map: Mapping[str, Any]) -> str:
    date_str = input_map.get("date")
    current_time = datetime.strptime(date_str, "%Y-%m-%d")
    file_name = get_log_file_name(current_time)
    if not os.path.isfile(file_name):
        return ""
    with open(file_name, "r") as f:
        return f.read()


text_input = StrInput(
    name="text",
    shortcut="t",
    prompt="Text",
    default="",
)

date_input = StrInput(
    name="date",
    shortcut="d",
    prompt="Date (Y-m-d)",
    default=CURRENT_TIME.strftime("%Y-%m-%d"),
)

content_input = MultilineInput(
    name="content",
    shortcut="c",
    comment_prefix="<!--",
    comment_suffix="-->",
    extension="md",
    default=_get_default_content,
)
