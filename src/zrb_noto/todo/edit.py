import os
from collections.abc import Mapping
from typing import Any

from zrb import Task, python_task, runner
from zrb.helper.task import show_lines

from .._config import IS_AUTO_SYNC, TODO_ABS_FILE_PATH
from ..sync import create_sync_noto_task
from ._group import noto_todo_group
from ._helper import get_pretty_todo_item_lines, get_todo_items
from ._input import content_input


def _get_content_default(input_map: Mapping[str, Any]) -> str:
    if not os.path.isfile(TODO_ABS_FILE_PATH):
        return ""
    with open(TODO_ABS_FILE_PATH, "r") as f:
        return f.read()


@python_task(
    name="save-file",
    inputs=[content_input],
    retry=0,
)
def save_file(*args, **kwargs):
    content = kwargs.get("content")
    with open(TODO_ABS_FILE_PATH, "w") as f:
        f.write(content)


@python_task(
    name="edit",
    group=noto_todo_group,
    inputs=[content_input],
    retry=0,
)
def edit_todo(*args, **kwargs):
    task: Task = kwargs.get("_task")
    show_lines(
        task,
        *get_pretty_todo_item_lines(get_todo_items(file_name=TODO_ABS_FILE_PATH)),
    )


if IS_AUTO_SYNC:
    (
        create_sync_noto_task(name="pre-sync")
        >> save_file
        >> create_sync_noto_task(name="post-sync")
        >> edit_todo
    )
else:
    save_file >> edit_todo

runner.register(edit_todo)
