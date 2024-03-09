from zrb import Task, python_task, runner
from zrb.helper.python_task import show_lines

from _automate.noto.todo._group import TODO_GROUP
from _automate.noto.todo._helper import get_items, get_pretty_item_lines


@python_task(
    name="list",
    group=TODO_GROUP,
    retry=0,
)
def list_todo(*args, **kwargs):
    task: Task = kwargs.get("_task")
    show_lines(
        task,
        *get_pretty_item_lines(get_items()),
    )


runner.register(list_todo)
