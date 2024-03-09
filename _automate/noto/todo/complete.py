from zrb import StrInput, Task, python_task, runner
from zrb.helper.accessories.color import colored
from zrb.helper.python_task import show_lines

from _automate.noto.log._helper import append_log, get_log, get_log_file_name
from _automate.noto.todo._group import TODO_GROUP
from _automate.noto.todo._helper import complete_item, get_items, get_pretty_lines


@python_task(
    name="complete",
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
def complete(*args, **kwargs):
    task: Task = kwargs.get("_task")
    search = kwargs.get("task")
    items = get_items(search=search, completed=False)
    if len(items) == 0:
        show_lines(
            task,
            colored("⚠️  NOT COMPLETED: Task not found", color="light_red"),
            "List of available tasks:",
            *get_pretty_lines(get_items(completed=False)),
        )
        return
    if len(items) > 1:
        show_lines(
            task,
            colored("⚠️  NOT COMPLETED: Multiple task found", color="light_red"),
            "List of matched tasks:",
            *get_pretty_lines(items),
        )
        return
    item = items[0]
    complete_item(item)
    append_log(f"__COMPLETE__ {item.description}")
    file_name = get_log_file_name()
    log_str = get_log(file_name)
    logs = log_str.split("\n")
    show_lines(task, *logs)


runner.register(complete)
