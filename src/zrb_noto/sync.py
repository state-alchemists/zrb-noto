import os
from typing import List, Optional

from zrb import Env, Group, Task, CmdTask, runner

from ._env import LOCAL_REPO_DIR_ENV, REMOTE_GIT_URL_ENV
from ._group import noto_group

_CURRENT_DIR = os.path.dirname(__file__)


def create_sync_noto_task(
    group: Optional[Group] = None,
    retry: int = 0,
    ignore_error: bool = True,
    upstreams: List[Task] = [],
) -> Task:
    sync_noto = CmdTask(
        name="sync",
        group=group,
        description="Sync noto",
        upstreams=upstreams,
        envs=[
            LOCAL_REPO_DIR_ENV, REMOTE_GIT_URL_ENV,
            Env(
                name="IGNORE_ERROR",
                os_name="",
                default="1" if ignore_error else "0"
            ),
        ],
        retry=retry,
        cmd_path=os.path.join(_CURRENT_DIR, "sync.sh"),
        should_show_cmd=False,
        should_print_cmd_result=False
    )
    return sync_noto


sync_noto = create_sync_noto_task(group=noto_group, ignore_error=False, retry=2)
runner.register(sync_noto)
