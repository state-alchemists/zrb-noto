from typing import Any

from zrb import Task, python_task, runner
from zrb.helper.task import show_lines

from ._group import noto_group
from ._helper import sync_noto
from .log._helper import get_pretty_log_lines
from .todo._helper import get_todo_items, get_pretty_todo_item_lines


@python_task(
    name="list",
    group=noto_group,
    description="List todo",
    retry=0,
)
def list_noto(*args: Any, **kwargs: Any):
    task: Task = kwargs.get("_task")
    sync_noto(task)
    items = get_todo_items(completed=False)
    show_lines(task, *get_pretty_log_lines(), "", *get_pretty_todo_item_lines(items))


runner.register(list_noto)
