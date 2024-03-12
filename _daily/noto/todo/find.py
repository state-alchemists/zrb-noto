from zrb import StrInput, Task, python_task, runner
from zrb.helper.python_task import show_lines

from _daily.noto._helper import sync_noto
from _daily.noto.todo._group import TODO_GROUP
from _daily.noto.todo._helper import (
    get_existing_contexts,
    get_existing_projects,
    get_items,
    get_pretty_item_lines,
)

_EXISTING_CONTEXT_STR = ",".join(get_existing_contexts())
_EXISTING_PROJECT_STR = ",".join(get_existing_projects())


@python_task(
    name="find",
    group=TODO_GROUP,
    inputs=[
        StrInput(
            name="search",
            prompt="Search pattern (regex)",
            default="",
        ),
        StrInput(
            name="project",
            prompt=f"Project, comma separated (e.g., {_EXISTING_PROJECT_STR})",
            default="",
        ),
        StrInput(
            name="context",
            prompt=f"Context, comma separated (e.g., {_EXISTING_CONTEXT_STR})",
            default="",
        ),
    ],
    retry=0,
)
def find(*args, **kwargs):
    task: Task = kwargs.get("_task")
    sync_noto(task)
    contexts = []
    context_str = kwargs.get("context")
    if context_str:
        contexts = [context.strip() for context in context_str.split(",")]
    projects = []
    project_str = kwargs.get("project")
    if project_str:
        projects = [project.strip() for project in project_str.split(",")]
    search = kwargs.get("search")
    show_lines(
        task,
        f"Projects: {projects}",
        f"Contexts: {contexts}",
        f"Search:   {search}",
        *get_pretty_item_lines(
            get_items(contexts=contexts, projects=projects, search=search)
        ),
    )


runner.register(find)
