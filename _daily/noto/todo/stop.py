from zrb import StrInput, Task, python_task, runner
from zrb.helper.accessories.color import colored
from zrb.helper.python_task import show_lines

from _daily.noto._helper import sync_noto
from _daily.noto.log._helper import append_log, get_pretty_log_lines
from _daily.noto.todo._group import TODO_GROUP
from _daily.noto.todo._helper import get_items, get_pretty_item_lines, stop_item


@python_task(
    name="stop",
    group=TODO_GROUP,
    inputs=[
        StrInput(
            name="task",
            shortcut="t",
            prompt="Search pattern (regex)",
            prompt_required=True,
            default="",
        ),
    ],
    retry=0,
)
def stop(*args, **kwargs):
    task: Task = kwargs.get("_task")
    sync_noto(task)
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
    stop_item(item)
    append_log(f"__STOP__ {item.description}")
    sync_noto(task)
    show_lines(task, *get_pretty_log_lines(), "", *get_pretty_item_lines(get_items()))


runner.register(stop)
