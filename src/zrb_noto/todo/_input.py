from zrb import StrInput

from .._config import CURRENT_DAY, CURRENT_MONTH, CURRENT_TIME, CURRENT_YEAR
from ._helper import get_existing_todo_contexts, get_existing_todo_projects

_EXISTING_CONTEXT_STR = ",".join(get_existing_todo_contexts())
_EXISTING_PROJECT_STR = ",".join(get_existing_todo_projects())

task_input = StrInput(
    name="task",
    shortcut="t",
    prompt="Task name or id",
    prompt_required=True,
    default="",
)

description_input = StrInput(
    name="description",
    prompt="Description",
    default="",
)

priority_input = StrInput(
    name="priority",
    prompt="Priority",
    default="C",
)

project_input = StrInput(
    name="project",
    prompt=f"Project, comma separated (e.g., {_EXISTING_PROJECT_STR})",
    default="",
)

context_input = StrInput(
    name="context",
    prompt=f"Context, comma separated (e.g., {_EXISTING_CONTEXT_STR})",
    default="",
)

keyval_input = StrInput(
    name="keyval",
    prompt=f"Keyval, comma separated (e.g., due:{CURRENT_YEAR}-{CURRENT_MONTH}-{CURRENT_DAY},jira:1234)",  # noqa
    default="",
)

date_input = StrInput(
    name="date",
    prompt="Date (Y-m-d)",
    default=CURRENT_TIME.strftime("%Y-%m-%d"),
)
