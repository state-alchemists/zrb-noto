from zrb import StrInput, Task, python_task, runner
from zrb.helper.accessories.color import colored
from zrb.helper.python_task import show_lines

from _daily.noto._config import CURRENT_DAY, CURRENT_MONTH, CURRENT_TIME, CURRENT_YEAR
from _daily.noto.todo._config import EXISTING_CONTEXT_STR, EXISTING_PROJECT_STR
from _daily.noto.todo._data import Item
from _daily.noto.todo._group import TODO_GROUP
from _daily.noto.todo._helper import (
    append_item,
    get_items,
    get_pretty_item_lines,
    read_keyval_input,
)


@python_task(
    name="add",
    group=TODO_GROUP,
    inputs=[
        StrInput(
            name="description",
            prompt="Description",
            default="",
        ),
        StrInput(
            name="priority",
            prompt="Priority",
            default="C",
        ),
        StrInput(
            name="project",
            prompt=f"Project, comma separated (e.g., {EXISTING_PROJECT_STR})",
            default="",
        ),
        StrInput(
            name="context",
            prompt=f"Context, comma separated (e.g., {EXISTING_CONTEXT_STR})",
            default="",
        ),
        StrInput(
            name="keyval",
            prompt=f"Keyval, comma separated (e.g., due:{CURRENT_YEAR}-{CURRENT_MONTH}-{CURRENT_DAY},jira:1234)",  # noqa
            default="",
        ),
    ],
    retry=0,
)
def add(*args, **kwargs):
    task: Task = kwargs.get("_task")
    description = kwargs.get("description")
    if description.strip() == "":
        task.print_err(colored("⚠️  NOT ADDED: Description cannot be empty"))
        return
    duplication = [item for item in get_items() if item.old_description == description]
    if len(duplication) > 0:
        task.print_err(
            colored(
                "⚠️  NOT ADDED: There is task with the same description",
                color="light_red",
            ),
        )
        return
    # priority
    priority = kwargs.get("priority")
    if priority.strip() == "":
        priority = "C"
    # contexts
    contexts = []
    context_str = kwargs.get("context")
    if context_str.strip() != "":
        contexts = [context.strip() for context in context_str.split(",")]
    # projects
    projects = []
    project_str = kwargs.get("project")
    if project_str.strip() != "":
        projects = [project.strip() for project in project_str.split(",")]
    # keyval
    keyval = {}
    keyval_input = kwargs.get("keyval")
    if keyval_input.strip() != "":
        keyval = read_keyval_input(keyval_input)
    keyval["createdAt"] = round(CURRENT_TIME.timestamp())
    item = Item(
        description=description,
        priority=priority,
        creation_date=CURRENT_TIME,
        contexts=contexts,
        projects=projects,
        keyval=keyval,
    )
    append_item(item=item)
    show_lines(task, *get_pretty_item_lines(get_items()))


runner.register(add)
