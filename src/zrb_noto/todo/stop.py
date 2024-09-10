from zrb import Task, python_task, runner
from zrb.helper.accessories.color import colored
from zrb.helper.task import show_lines

from .._config import CURRENT_TIME, IS_AUTO_SYNC, TODO_ABS_FILE_PATH
from ..log._helper import append_log_item, get_log_file_name, get_pretty_log_lines
from ..sync import create_sync_noto_task
from ._group import noto_todo_group
from ._helper import get_pretty_todo_item_lines, get_todo_items, stop_todo_item
from ._input import task_input


@python_task(
    name="stop-item",
    group=noto_todo_group,
    inputs=[task_input],
    retry=0,
)
def stop_item(*args, **kwargs):
    task: Task = kwargs.get("_task")
    search = kwargs.get("task")
    items = get_todo_items(file_name=TODO_ABS_FILE_PATH, search=search, completed=False)
    if len(items) == 0:
        show_lines(
            task,
            colored("⚠️  NOT STOPPED: Task not found", color="light_red"),
            "List of available tasks:",
            *get_pretty_todo_item_lines(
                get_todo_items(file_name=TODO_ABS_FILE_PATH, completed=False)
            ),
        )
        return
    if len(items) > 1:
        show_lines(
            task,
            colored("⚠️  NOT STOPPED: Multiple task found", color="light_red"),
            "List of matched tasks:",
            *get_pretty_todo_item_lines(items),
        )
        return
    item = items[0]
    task.print_out(colored(f"Stopping task: {item.description}", color="yellow"))
    stop_todo_item(file_name=TODO_ABS_FILE_PATH, item=item)
    append_log_item(
        f"__STOP__ [{item.get_id()}] {item.description}", current_time=CURRENT_TIME
    )


@python_task(
    name="stop",
    group=noto_todo_group,
    inputs=[task_input],
    retry=0,
)
def stop_todo(*args, **kwargs):
    task: Task = kwargs.get("_task")
    show_lines(
        task,
        *get_pretty_log_lines(file_name=get_log_file_name(current_time=CURRENT_TIME)),
        "",
        *get_pretty_todo_item_lines(get_todo_items(file_name=TODO_ABS_FILE_PATH)),
    )


if IS_AUTO_SYNC:
    (
        create_sync_noto_task(name="pre-sync")
        >> stop_item
        >> create_sync_noto_task(name="post-sync")
        >> stop_todo
    )
else:
    stop_item >> stop_todo

runner.register(stop_todo)
