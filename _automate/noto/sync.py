import os
from typing import Any

from zrb import Task, python_task, runner

from _automate.noto._config import CURRENT_DIR
from _automate.noto._env import PROJECT_DIR_ENV
from _automate.noto._group import NOTO_GROUP
from _automate.noto._helper import run_cmd_path
from _automate.noto.lint import lint


@python_task(
    name="sync",
    group=NOTO_GROUP,
    description="sync code",
    upstreams=[lint],
    envs=[PROJECT_DIR_ENV],
)
def sync(*args: Any, **kwargs: Any):
    task: Task = kwargs.get("_task")
    run_cmd_path(task, os.path.join(CURRENT_DIR, "sync.sh"))


runner.register(sync)
