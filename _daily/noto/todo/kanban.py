from zrb import Task, python_task, runner
from zrb.helper.python_task import show_lines

from _daily.noto.todo._group import TODO_GROUP
from _daily.noto.todo._helper import get_items, get_kanban_lines


@python_task(
    name="kanban",
    group=TODO_GROUP,
    retry=0,
)
def kanban(*args, **kwargs):
    task: Task = kwargs.get("_task")
    show_lines(
        task,
        *get_kanban_lines(get_items()),
    )


runner.register(kanban)