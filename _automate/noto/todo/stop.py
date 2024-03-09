from zrb import StrInput, Task, python_task, runner
from zrb.helper.accessories.color import colored
from zrb.helper.python_task import show_lines

from _automate.noto.log._helper import append_log, get_log_lines
from _automate.noto.todo._group import TODO_GROUP
from _automate.noto.todo._helper import get_items, get_pretty_item_lines


@python_task(
    name="stop",
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
def stop(*args, **kwargs):
    task: Task = kwargs.get("_task")
    search = kwargs.get("task")
    items = get_items(search=search, completed=False)
    if len(items) == 0:
        show_lines(
            task,
            colored("⚠️  NOT STOPPED: Task not found", color="light_red"),
            "List of available tasks:",
            *get_pretty_item_lines(get_items(completed=False)),
        )
        return
    if len(items) > 1:
        show_lines(
            task,
            colored("⚠️  NOT STOPPED: Multiple task found", color="light_red"),
            "List of matched tasks:",
            *get_pretty_item_lines(items),
        )
        return
    item = items[0]
    append_log(f"__STOP__ {item.description}")
    show_lines(task, *get_log_lines())


runner.register(stop)
