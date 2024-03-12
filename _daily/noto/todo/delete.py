from zrb import StrInput, Task, python_task, runner
from zrb.helper.accessories.color import colored
from zrb.helper.python_task import show_lines

from _daily.noto._helper import sync_noto
from _daily.noto.todo._group import TODO_GROUP
from _daily.noto.todo._helper import delete_item, get_items, get_pretty_item_lines


@python_task(
    name="delete",
    group=TODO_GROUP,
    inputs=[
        StrInput(
            name="task",
            prompt="Search pattern (regex)",
            prompt_required=True,
            default="",
        ),
    ],
    retry=0,
)
def delete(*args, **kwargs):
    task: Task = kwargs.get("_task")
    sync_noto(task)
    search = kwargs.get("task")
    items = get_items(search=search)
    if len(items) == 0:
        show_lines(
            task,
            colored("⚠️  NOT DELETED: Task not found", color="light_red"),
            "List of available tasks:",
            *get_pretty_item_lines(get_items()),
        )
        return
    if len(items) > 1:
        show_lines(
            task,
            colored("⚠️  NOT DELETED: Multiple task found", color="light_red"),
            "List of matched tasks:",
            *get_pretty_item_lines(items),
        )
        return
    item = items[0]
    delete_item(item)
    sync_noto(task)
    show_lines(task, *get_pretty_item_lines(get_items()))


runner.register(delete)
