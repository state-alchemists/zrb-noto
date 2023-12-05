from typing import Any
from zrb import runner, CmdTask
from .._group import noto_git_group
from ..config import NOTO_MACHINE_NAME
from .fetch import git_fetch
import os
import datetime

CURRENT_DIR = os.path.dirname(__file__)
NOTO_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))


def _git_commit_cmd(*args: Any, **kwargs: Any):
    now = datetime.datetime.now().isoformat()
    message = f'{NOTO_MACHINE_NAME}: Update on {now}'
    return [
        'if git diff-index --quiet HEAD --; then',
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
