from zrb import StrInput, Task, python_task, runner
from zrb.helper.accessories.color import colored
from zrb.helper.task import show_lines

from .._config import CURRENT_TIME, IS_AUTO_SYNC
from ..sync import create_sync_noto_task
from ._data import Item
from ._group import noto_todo_group
from ._helper import (
    append_todo_item,
    get_pretty_todo_item_lines,
    get_todo_items,
    read_keyval_input,
)
from ._input import (
    context_input,
    date_input,
    keyval_input,
    priority_input,
    project_input,
)

new_description_input = StrInput(
    name="description",
    shortcut="t",
    prompt="Description",
    default="",
)


@python_task(
    name="add-item",
    inputs=[
        new_description_input,
        priority_input,
        project_input,
        context_input,
        keyval_input,
        date_input,
    ],
    retry=0,
)
def add_item(*args, **kwargs):
    task: Task = kwargs.get("_task")
    description = kwargs.get("description")
    if description.strip() == "":
        task.print_err(colored("⚠️  NOT ADDED: Description cannot be empty"))
        return
    duplication = [
        item for item in get_todo_items() if item.old_description == description
    ]
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
    task.print_out(colored(f"Adding task: {item.description}", color="yellow"))
    append_todo_item(item=item)


@python_task(
    name="add",
    group=noto_todo_group,
    inputs=[
        new_description_input,
        priority_input,
        project_input,
        context_input,
        keyval_input,
        date_input,
    ],
    retry=0,
)
def add_todo(*args, **kwargs):
    task: Task = kwargs.get("_task")
    show_lines(task, *get_pretty_todo_item_lines(get_todo_items()))


if IS_AUTO_SYNC:
    (
        create_sync_noto_task(name="pre-sync")
        >> add_item
        >> create_sync_noto_task(name="post-sync")
        >> add_todo
    )
else:
    add_item >> add_todo
runner.register(add_todo)
