from datetime import datetime

from zrb import StrInput, Task, python_task, runner
from zrb.helper.python_task import show_lines

from _automate.noto._config import CURRENT_TIME
from _automate.noto.todo._group import TODO_GROUP
from _automate.noto.todo._helper import Item, append_item, get_items


@python_task(
    name="add",
    group=TODO_GROUP,
    inputs=[
        StrInput(
            name="date",
            prompt="Date (Y-m-d H:M)",
            default=CURRENT_TIME.strftime("%Y-%m-%d %H:%M"),
        ),
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
            name="context",
            prompt="Context, comma separated",
            default="",
        ),
        StrInput(
            name="project",
            prompt="Project, comma separated",
            default="personal",
        ),
    ],
)
def add(*args, **kwargs):
    task: Task = kwargs.get("_task")
    date_str = kwargs.get("date")
    creation_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    description = kwargs.get("description")
    priority = kwargs.get("priority")
    if not priority:
        priority = None
    contexts = []
    context_str = kwargs.get("context")
    if context_str:
        contexts = [context.strip() for context in context_str.split(",")]
    projects = []
    project_str = kwargs.get("project")
    if project_str:
        projects = [project.strip() for project in project_str.split(",")]
    item = Item(
        description=description,
        priority=priority,
        creation_date=creation_date,
        contexts=contexts,
        projects=projects,
    )
    append_item(item=item)
    items = get_items()
    lines = [item.as_str(show_empty=True, show_color=True) for item in items]
    show_lines(task, *lines)


runner.register(add)
