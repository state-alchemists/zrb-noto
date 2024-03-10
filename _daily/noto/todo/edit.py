from zrb import StrInput, Task, python_task, runner
from zrb.helper.accessories.color import colored
from zrb.helper.python_task import show_lines

from _daily.noto._config import CURRENT_DAY, CURRENT_MONTH, CURRENT_YEAR
from _daily.noto.todo._group import TODO_GROUP
from _daily.noto.todo._helper import (
    get_existing_contexts,
    get_existing_projects,
    get_items,
    get_pretty_item_lines,
    read_keyval_input,
    replace_item,
)

_EXISTING_CONTEXT_STR = ",".join(get_existing_contexts())
_EXISTING_PROJECT_STR = ",".join(get_existing_projects())


@python_task(
    name="edit",
    group=TODO_GROUP,
    inputs=[
        StrInput(
            name="task",
            prompt="Task",
            default="",
        ),
        StrInput(
            name="description",
            prompt="New description",
            default="",
        ),
        StrInput(
            name="priority",
            prompt="New priority",
            default="",
        ),
        StrInput(
            name="project",
            prompt=f"New project, comma separated (e.g., {_EXISTING_PROJECT_STR})",
            default="",
        ),
        StrInput(
            name="context",
            prompt=f"New context, comma separated (e.g., {_EXISTING_CONTEXT_STR})",
            default="",
        ),
        StrInput(
            name="keyval",
            prompt=f"New keyval, comma separated (e.g., due:{CURRENT_YEAR}-{CURRENT_MONTH}-{CURRENT_DAY},jira:1234)",  # noqa
            default="",
        ),
    ],
    retry=0,
)
def edit(*args, **kwargs):
    task: Task = kwargs.get("_task")
    # Getting the item
    search = kwargs.get("task")
    items = get_items(search=search, completed=False)
    if len(items) == 0:
        show_lines(
            task,
            colored("⚠️  NOT COMPLETED: Task not found", color="light_red"),
            "List of available tasks:",
            *get_pretty_item_lines(get_items(completed=False)),
        )
        return
    if len(items) > 1:
        show_lines(
            task,
            colored("⚠️  NOT COMPLETED: Multiple task found", color="light_red"),
            "List of matched tasks:",
            *get_pretty_item_lines(items),
        )
        return
    item = items[0]
    # description
    description = kwargs.get("description")
    if description.strip() != "":
        duplication = [
            item for item in get_items() if item.old_description == description
        ]
        if len(duplication) > 0:
            task.print_err(
                colored(
                    "⚠️  NOT ADDED: There is task with the same description",
                    color="light_red",
                ),
            )
            return
        item.description = description
    # priority
    priority = kwargs.get("priority")
    if priority.strip() != "":
        item.priority = priority
    # contexts
    context_str = kwargs.get("context")
    if context_str.strip() != "":
        item.contexts = [context.strip() for context in context_str.split(",")]
    # projects
    project_str = kwargs.get("project")
    if project_str.strip() != "":
        item.projects = [project.strip() for project in project_str.split(",")]
    # keyval
    keyval_input = kwargs.get("keyval")
    if keyval_input.strip() != "":
        item.keyval = read_keyval_input(keyval_input)
    # save item
    replace_item(item)
    show_lines(task, *get_pretty_item_lines(get_items()))


runner.register(edit)
