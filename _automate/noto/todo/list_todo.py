from zrb import StrInput, Task, python_task, runner
from zrb.helper.python_task import show_lines

from _automate.noto.todo._group import TODO_GROUP
from _automate.noto.todo._helper import get_items


@python_task(
    name="list",
    group=TODO_GROUP,
    inputs=[
        StrInput(
            name="context",
            prompt="Context, comma separated",
            default="",
        ),
        StrInput(
            name="project",
            prompt="Project, comma separated",
            default="",
        ),
    ],
)
def list_todo(*args, **kwargs):
    task: Task = kwargs.get("_task")
    contexts = []
    context_str = kwargs.get("context")
    if context_str:
        contexts = [context.strip() for context in context_str.split(",")]
    projects = []
    project_str = kwargs.get("project")
    if project_str:
        projects = [project.strip() for project in project_str.split(",")]
    items = get_items()
    lines = [item.as_str(show_empty=True, show_color=True) for item in items]
    show_lines(task, f"Contexts: {contexts}", f"Projects: {projects}", *lines)


runner.register(list_todo)
