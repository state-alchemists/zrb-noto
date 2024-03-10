import os
from typing import Any

from zrb import Task, python_task, runner

from _daily.noto._config import CURRENT_DIR
from _daily.noto._env import PROJECT_DIR_ENV
from _daily.noto._group import NOTO_GROUP
from _daily.noto._helper import run_cmd_path


@python_task(
    name="lint", group=NOTO_GROUP, description="Lint code", envs=[PROJECT_DIR_ENV]
)
def lint(*args: Any, **kwargs: Any):
    task: Task = kwargs.get("_task")
    run_cmd_path(task, os.path.join(CURRENT_DIR, "lint.sh"))


runner.register(lint)