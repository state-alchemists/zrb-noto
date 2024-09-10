from zrb import Task, python_task, runner
from zrb.helper.accessories.color import colored
from zrb.helper.task import show_lines

from .._config import CURRENT_TIME, IS_AUTO_SYNC, TODO_ABS_FILE_PATH
from ..log._helper import append_log_item, get_pretty_log_lines
from ..sync import create_sync_noto_task
from ._group import noto_todo_group
from ._helper import delete_todo_item, get_pretty_todo_item_lines, get_todo_items
from ._input import task_input


@python_task(
    name="delete-item",
    inputs=[task_input],
    retry=0,
)
def delete_item(*args, **kwargs):
    task: Task = kwargs.get("_task")
    search = kwargs.get("task")
    items = get_todo_items(file_name=TODO_ABS_FILE_PATH, search=search)
    if len(items) == 0:
        show_lines(
            task,
            colored("⚠️  NOT DELETED: Task not found", color="light_red"),
            "List of available tasks:",
            *get_pretty_todo_item_lines(get_todo_items(file_name=TODO_ABS_FILE_PATH)),
        )
        return
    if len(items) > 1:
        show_lines(
            task,
            colored("⚠️  NOT DELETED: Multiple task found", color="light_red"),
            "List of matched tasks:",
            *get_pretty_todo_item_lines(items),
        )
        return
    item = items[0]
    task.print_out(colored(f"Deleting task: {item.description}", color="yellow"))
    delete_todo_item(file_name=TODO_ABS_FILE_PATH, item=item)
    append_log_item(f"__DELETE__ [{item.get_id()}] {item.description}", CURRENT_TIME)


@python_task(
    name="delete",
    group=noto_todo_group,
    inputs=[task_input],
    retry=0,
)
def delete_todo(*args, **kwargs):
    task: Task = kwargs.get("_task")
    show_lines(
        task,
        *get_pretty_log_lines(file_name=TODO_ABS_FILE_PATH),
        "",
        *get_pretty_todo_item_lines(get_todo_items(file_name=TODO_ABS_FILE_PATH)),
    )


if IS_AUTO_SYNC:
    (
        create_sync_noto_task(name="pre-sync")
        >> delete_item
        >> create_sync_noto_task(name="post-sync")
        >> delete_todo
    )
else:
    delete_item >> delete_todo

runner.register(delete_todo)
