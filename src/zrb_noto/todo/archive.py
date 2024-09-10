from zrb import StrInput, Task, python_task, runner
from zrb.helper.task import show_lines

from .._config import DONE_ABS_FILE_PATH, IS_AUTO_SYNC, TODO_ABS_FILE_PATH
from ..log._helper import get_pretty_log_lines
from ..sync import create_sync_noto_task
from ._group import noto_todo_group
from ._helper import get_pretty_todo_item_lines, get_todo_items, save_items

new_description_input = StrInput(
    name="description",
    shortcut="t",
    prompt="Description",
    default="",
)


@python_task(
    name="archive-item",
    retry=0,
)
def archive_item(*args, **kwargs):
    todo_items = get_todo_items(file_name=TODO_ABS_FILE_PATH)
    archived_todo_items = get_todo_items(file_name=DONE_ABS_FILE_PATH)
    completed_todo_items = [
        item for item in todo_items if item.get_status() == "COMPLETED"
    ]
    incompleted_todo_items = [
        item for item in todo_items if item.get_status() != "COMPLETED"
    ]
    todo_items = incompleted_todo_items
    archived_todo_items += completed_todo_items
    save_items(file_name=DONE_ABS_FILE_PATH, items=archived_todo_items)
    save_items(file_name=TODO_ABS_FILE_PATH, items=todo_items)


@python_task(
    name="archive",
    group=noto_todo_group,
    retry=0,
)
def archive_todo(*args, **kwargs):
    task: Task = kwargs.get("_task")
    show_lines(
        task,
        *get_pretty_log_lines(file_name=TODO_ABS_FILE_PATH),
        "",
        *get_pretty_todo_item_lines(get_todo_items(file_name=TODO_ABS_FILE_PATH))
    )


if IS_AUTO_SYNC:
    (
        create_sync_noto_task(name="pre-sync")
        >> archive_item
        >> create_sync_noto_task(name="post-sync")
        >> archive_todo
    )
else:
    archive_item >> archive_todo

runner.register(archive_todo)
