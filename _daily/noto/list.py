from typing import Any

from zrb import Task, python_task, runner
from zrb.helper.python_task import show_lines

from _daily.noto._env import PROJECT_DIR_ENV
from _daily.noto._group import NOTO_GROUP
from _daily.noto._helper import sync_noto
from _daily.noto.log._helper import get_pretty_log_lines
from _daily.noto.todo._helper import get_items, get_pretty_item_lines


@python_task(
    name="list",
    group=NOTO_GROUP,
    description="List todo",
    envs=[PROJECT_DIR_ENV],
    retry=0,
)
def list(*args: Any, **kwargs: Any):
    task: Task = kwargs.get("_task")
    sync_noto(task)
    items = get_items(completed=False)
    show_lines(task, *get_pretty_log_lines(), "", *get_pretty_item_lines(items))


runner.register(list)
