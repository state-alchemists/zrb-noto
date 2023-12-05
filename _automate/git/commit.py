from typing import Any
from zrb import runner, CmdTask
from .._group import noto_git_group
from ..config import NOTO_MACHINE_NAME
from .add import git_add
import os
import datetime

CURRENT_DIR = os.path.dirname(__file__)
NOTO_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))


def _git_commit_cmd(*args: Any, **kwargs: Any):
    now = datetime.datetime.now().isoformat()
    message = f'{NOTO_MACHINE_NAME}: Update on {now}'
    return [
        'set -e',
        f'git commit -m "{message}"'
    ]


git_commit = CmdTask(
    name='commit',
    group=noto_git_group,
    upstreams=[git_add],
    cwd=NOTO_DIR,
    cmd=_git_commit_cmd()
)
runner.register(git_commit)
