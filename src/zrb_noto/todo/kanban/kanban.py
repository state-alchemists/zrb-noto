from zrb import Task, python_task, runner
from zrb.helper.task import show_lines

from ..._config import IS_AUTO_SYNC, TODO_ABS_FILE_PATH
from ..._helper import get_screen_width
from ...sync import create_sync_noto_task, sync_noto
from .._group import noto_todo_group
from .._helper import get_todo_items
from ._helper import get_kanban_lines


@python_task(
    name="kanban",
    group=noto_todo_group,
    upstreams=[sync_noto],
    retry=0,
)
def show_kanban(*args, **kwargs):
    task: Task = kwargs.get("_task")
    items = get_todo_items(file_name=TODO_ABS_FILE_PATH)
    screen_width = get_screen_width()
    show_lines(
        task,
        *get_kanban_lines(items, screen_width),
    )


if IS_AUTO_SYNC:
    create_sync_noto_task(name="pre-sync") >> show_kanban

runner.register(show_kanban)
