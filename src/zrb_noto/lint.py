import os
from typing import Any

from zrb import Task, python_task, runner

from ._env import LOCAL_REPO_DIR_ENV
from ._group import noto_group
from ._helper import run_cmd_path

_CURRENT_DIR = os.path.dirname(__file__)


@python_task(
    name="lint", group=noto_group, description="Lint code", envs=[LOCAL_REPO_DIR_ENV]
)
def lint_noto(*args: Any, **kwargs: Any):
    task: Task = kwargs.get("_task")
    run_cmd_path(task, os.path.join(_CURRENT_DIR, "lint.sh"))


runner.register(lint_noto)
