from zrb import StrInput, Task, python_task, runner
from zrb.helper.python_task import show_lines

from _automate.noto.todo._config import EXISTING_CONTEXT_STR, EXISTING_PROJECT_STR
from _automate.noto.todo._group import TODO_GROUP
from _automate.noto.todo._helper import get_items


@python_task(
    name="list",
    group=TODO_GROUP,
    inputs=[
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
            name="keyword",
            prompt="Keyword",
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
    keyword = kwargs.get("keyword")
    items = get_items(contexts=contexts, projects=projects, keyword=keyword)
    lines = [item.as_pretty_str() for item in items]
    show_lines(task, f"Projects: {projects}", f"Contexts: {contexts}", *lines)


runner.register(list_todo)
