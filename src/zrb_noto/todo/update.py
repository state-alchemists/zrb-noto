from zrb import StrInput, Task, python_task, runner
from zrb.helper.accessories.color import colored
from zrb.helper.task import show_lines

from .._config import CURRENT_TIME, IS_AUTO_SYNC, TODO_ABS_FILE_PATH
from ..log._helper import append_log_item, get_log_file_name, get_pretty_log_lines
from ..sync import create_sync_noto_task
from ._group import noto_todo_group
from ._helper import (
    get_pretty_todo_item_lines,
    get_todo_items,
    read_keyval_input,
    replace_todo_item,
)
from ._input import (
    context_input,
    date_input,
    description_input,
    keyval_input,
    project_input,
    task_input,
)

priority_input = StrInput(
    name="priority",
    prompt="Priority",
    default="",
)


@python_task(
    name="edit_item",
    inputs=[
        task_input,
        description_input,
        priority_input,
        project_input,
        context_input,
        keyval_input,
        date_input,
    ],
    retry=0,
)
def edit_item(*args, **kwargs):
    task: Task = kwargs.get("_task")
    # Getting the item
    search = kwargs.get("task")
    items = get_todo_items(file_name=TODO_ABS_FILE_PATH, search=search, completed=False)
    if len(items) == 0:
        show_lines(
            task,
            colored("⚠️  NOT COMPLETED: Task not found", color="light_red"),
            "List of available tasks:",
            *get_pretty_todo_item_lines(
                get_todo_items(file_name=TODO_ABS_FILE_PATH, completed=False)
            ),
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
    # description
    description = kwargs.get("description")
    if description.strip() != "":
        duplication = [
            item
            for item in get_todo_items(file_name=TODO_ABS_FILE_PATH)
            if item.old_description == description
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
        item.set_keyval(read_keyval_input(keyval_input))
    # save item
    task.print_out(colored(f"Editing task: {item.description}", color="yellow"))
    replace_todo_item(file_name=TODO_ABS_FILE_PATH, item=item)
    append_log_item(
        f"__EDIT__ [{item.get_id()}] {item.description}", current_time=CURRENT_TIME
    )


@python_task(
    name="update",
    group=noto_todo_group,
    inputs=[
        task_input,
        description_input,
        priority_input,
        project_input,
        context_input,
        keyval_input,
        date_input,
    ],
    retry=0,
)
def update_todo(*args, **kwargs):
    task: Task = kwargs.get("_task")
    show_lines(
        task,
        *get_pretty_log_lines(file_name=get_log_file_name(CURRENT_TIME)),
        "",
        *get_pretty_todo_item_lines(get_todo_items(file_name=TODO_ABS_FILE_PATH)),
    )


if IS_AUTO_SYNC:
    (
        create_sync_noto_task(name="pre-sync")
        >> edit_item
        >> create_sync_noto_task(name="post-sync")
        >> update_todo
    )
else:
    edit_item >> update_todo

runner.register(update_todo)
