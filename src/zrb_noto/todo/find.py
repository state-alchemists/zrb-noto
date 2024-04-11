from zrb import Task, python_task, runner
from zrb.helper.task import show_lines

from ..sync import create_sync_noto_task
from ._group import noto_todo_group
from ._helper import get_pretty_todo_item_lines, get_todo_items
from ._input import context_input, project_input, task_input


@python_task(
    name="find",
    group=noto_todo_group,
    inputs=[task_input, project_input, context_input],
    retry=0,
)
def find_todo(*args, **kwargs):
    task: Task = kwargs.get("_task")
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
        *get_pretty_todo_item_lines(
            get_todo_items(contexts=contexts, projects=projects, search=search)
        ),
    )


create_sync_noto_task(name="pre-sync") >> find_todo
runner.register(find_todo)
