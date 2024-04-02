from zrb import Task, python_task, runner
from zrb.helper.task import show_lines

from _daily.noto._env import PROJECT_DIR_ENV
from _daily.noto._helper import sync_noto
from _daily.noto.todo._group import TODO_GROUP
from _daily.noto.todo._helper import get_items, get_pretty_item_lines


@python_task(
    name="list",
    group=TODO_GROUP,
    envs=[PROJECT_DIR_ENV],
    retry=0,
)
def list_todo(*args, **kwargs):
    task: Task = kwargs.get("_task")
    sync_noto(task)
    show_lines(
        task,
        *get_pretty_item_lines(get_items()),
    )


runner.register(list_todo)
