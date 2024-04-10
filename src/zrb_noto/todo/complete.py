from zrb import Task, python_task, runner
from zrb.helper.accessories.color import colored
from zrb.helper.task import show_lines

from ..log._helper import append_log_item, get_pretty_log_lines
from ..sync import create_sync_noto_task
from ._group import noto_todo_group
from ._helper import complete_todo_item, get_pretty_todo_item_lines, get_todo_items
from ._input import task_input


@python_task(
    name="complete-item",
    inputs=[task_input],
    retry=0,
)
def complete_item(*args, **kwargs):
    task: Task = kwargs.get("_task")
    search = kwargs.get("task")
    items = get_todo_items(search=search, completed=False)
    if len(items) == 0:
        show_lines(
            task,
            colored("⚠️  NOT COMPLETED: Task not found", color="light_red"),
            "List of available tasks:",
            *get_pretty_todo_item_lines(get_todo_items(completed=False)),
        )
        return
    if len(items) > 1:
        show_lines(
            task,
            colored("⚠️  NOT COMPLETED: Multiple task found", color="light_red"),
            "List of matched tasks:",
            *get_pretty_todo_item_lines(items),
        )
        return
    item = items[0]
    complete_todo_item(item)
    append_log_item(f"__COMPLETE__ {item.description}")


@python_task(
    name="complete",
    group=noto_todo_group,
    inputs=[task_input],
    retry=0,
)
def complete_todo(*args, **kwargs):
    task: Task = kwargs.get("_task")
    show_lines(
        task, *get_pretty_log_lines(), "", *get_pretty_todo_item_lines(get_todo_items())
    )


create_sync_noto_task() >> complete_item >> create_sync_noto_task() >> complete_todo
runner.register(complete_todo)
