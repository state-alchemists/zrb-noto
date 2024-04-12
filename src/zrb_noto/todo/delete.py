from zrb import Task, python_task, runner
from zrb.helper.accessories.color import colored
from zrb.helper.task import show_lines

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
    items = get_todo_items(search=search)
    if len(items) == 0:
        show_lines(
            task,
            colored("⚠️  NOT DELETED: Task not found", color="light_red"),
            "List of available tasks:",
            *get_pretty_todo_item_lines(get_todo_items()),
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
    delete_todo_item(item)


@python_task(
    name="delete",
    group=noto_todo_group,
    inputs=[task_input],
    retry=0,
)
def delete_todo(*args, **kwargs):
    task: Task = kwargs.get("_task")
    show_lines(task, *get_pretty_todo_item_lines(get_todo_items()))


create_sync_noto_task(name="pre-sync") >> delete_item >> create_sync_noto_task(name="post-sync") >> delete_todo  # noqa
runner.register(delete_todo)
