import os
from typing import List, Optional

from zrb import CmdTask, Env, Group, StrInput, Task, runner

from ._env import LOCAL_REPO_DIR_ENV, REMOTE_GIT_URL_ENV
from ._group import noto_group

_CURRENT_DIR = os.path.dirname(__file__)


def create_sync_noto_task(
    name: str = "sync",
    group: Optional[Group] = None,
    retry: int = 0,
    ignore_error: bool = True,
    upstreams: List[Task] = [],
    custom_commit_message: bool = False,
) -> Task:
    sync_noto = CmdTask(
        name=name,
        group=group,
        description="Sync noto",
        upstreams=upstreams,
        envs=[
            LOCAL_REPO_DIR_ENV,
            REMOTE_GIT_URL_ENV,
            Env(
                name="IGNORE_ERROR",
                os_name="",
                default="1" if ignore_error else "0"
            ),
            Env(
                name="COMMIT_MESSAGE",
                os_name="",
                default="{{input.commit_message}}"
            ),
        ],
        retry=retry,
        cmd_path=os.path.join(_CURRENT_DIR, "sync.sh"),
        should_show_cmd=False,
        should_print_cmd_result=False,
    )
    if custom_commit_message:
        sync_noto.add_input(
            StrInput(
                name="commit-message",
                prompt="Commit message, if any (can be empty)",
                default="",
            ),
        )
    return sync_noto


sync_noto = create_sync_noto_task(
    group=noto_group, ignore_error=False, custom_commit_message=True, retry=2
)
runner.register(sync_noto)
