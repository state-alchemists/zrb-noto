import os
from collections.abc import Mapping
from typing import Any

from zrb import MultilineInput, StrInput

from .._config import (
    CURRENT_DAY,
    CURRENT_MONTH,
    CURRENT_TIME,
    CURRENT_YEAR,
    TODO_ABS_FILE_PATH,
)
from ._helper import get_existing_todo_contexts, get_existing_todo_projects

_EXISTING_CONTEXT_STR = ",".join(
    get_existing_todo_contexts(file_name=TODO_ABS_FILE_PATH)
)
_EXISTING_PROJECT_STR = ",".join(
    get_existing_todo_projects(file_name=TODO_ABS_FILE_PATH)
)


def _get_default_content(input_map: Mapping[str, Any]) -> str:
    if not os.path.isfile(TODO_ABS_FILE_PATH):
        return ""
    with open(TODO_ABS_FILE_PATH, "r") as f:
        return f.read()


task_input = StrInput(
    name="task",
    shortcut="t",
    prompt="Task name or id",
    prompt_required=True,
    default="",
)

description_input = StrInput(
    name="description",
    prompt="Description",
    default="",
)

priority_input = StrInput(
    name="priority",
    prompt="Priority",
    default="C",
)

project_input = StrInput(
    name="project",
    prompt=f"Project, comma separated (e.g., {_EXISTING_PROJECT_STR})",
    default="",
)

context_input = StrInput(
    name="context",
    prompt=f"Context, comma separated (e.g., {_EXISTING_CONTEXT_STR})",
    default="",
)

keyval_input = StrInput(
    name="keyval",
    prompt=f"Keyval, comma separated (e.g., due:{CURRENT_YEAR}-{CURRENT_MONTH}-{CURRENT_DAY},jira:1234)",  # noqa
    default="",
)

date_input = StrInput(
    name="date",
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
