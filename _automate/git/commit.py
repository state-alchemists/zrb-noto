from typing import Any
from zrb import runner, CmdTask
from .._group import noto_git_group
from ..config import NOTO_MACHINE_NAME, NOTO_GIT_REMOTE_NAME
from ._helper import get_current_branch
from .fetch import git_fetch
import os
import datetime

CURRENT_DIR = os.path.dirname(__file__)
NOTO_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))


def _git_commit_cmd(*args: Any, **kwargs: Any):
    now = datetime.datetime.now().isoformat()
    remote_name = NOTO_GIT_REMOTE_NAME
    branch = get_current_branch
    message = f'{NOTO_MACHINE_NAME}: Update on {now}'
    return [
        f'if git diff-index --quiet {remote_name}/{branch} --; then',
        '    echo "No changes to commit."',
        'else',
        '    git add .',
        f'    git commit -m "{message}"',
        'fi'
    ]


git_commit = CmdTask(
    name='commit',
    group=noto_git_group,
    upstreams=[git_fetch],
    cwd=NOTO_DIR,
    cmd=_git_commit_cmd
)
runner.register(git_commit)
