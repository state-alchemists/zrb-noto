from zrb import Task, python_task, runner
from zrb.helper.task import show_lines

from _daily.noto._env import PROJECT_DIR_ENV
from _daily.noto._helper import sync_noto, get_screen_width
from _daily.noto.todo._group import TODO_GROUP
from _daily.noto.todo._helper import get_items
from _daily.noto.todo.kanban._helper import get_kanban_lines


@python_task(
    name="kanban",
    group=TODO_GROUP,
    envs=[PROJECT_DIR_ENV],
    retry=0,
)
def kanban(*args, **kwargs):
    task: Task = kwargs.get("_task")
    sync_noto(task)
    items = get_items()
    screen_width = get_screen_width()
    show_lines(
        task,
        *get_kanban_lines(items, screen_width),
    )


runner.register(kanban)
