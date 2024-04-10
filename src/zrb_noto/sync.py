import os
from typing import Any, List, Optional

from zrb import Group, Task, python_task, runner

from ._env import LOCAL_REPO_DIR_ENV, REMOTE_GIT_URL_ENV
from ._group import noto_group
from ._helper import run_cmd_path

_CURRENT_DIR = os.path.dirname(__file__)


def create_sync_noto_task(
    group: Optional[Group] = None,
    retry: int = 0,
    ignore_error: bool = True,
    upstreams: List[Task] = [],
) -> Task:
    @python_task(
        name="sync",
        group=group,
        description="Sync noto",
        upstreams=upstreams,
        envs=[LOCAL_REPO_DIR_ENV, REMOTE_GIT_URL_ENV],
        retry=retry,
    )
    def sync_noto(*args: Any, **kwargs: Any):
        task: Task = kwargs.get("_task")
        try:
            run_cmd_path(task, os.path.join(_CURRENT_DIR, "sync.sh"))
        except Exception as e:
            if not ignore_error:
                raise e

    return sync_noto


sync_noto = create_sync_noto_task(group=noto_group, ignore_error=False, retry=3)
runner.register(sync_noto)
