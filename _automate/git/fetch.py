from zrb import runner, CmdTask
from .._group import noto_git_group
from ..config import NOTO_GIT_REMOTE_NAME
import os

CURRENT_DIR = os.path.dirname(__file__)
NOTO_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))

git_fetch = CmdTask(
    name='fetch',
    group=noto_git_group,
    cwd=NOTO_DIR,
    cmd=f'git fetch {NOTO_GIT_REMOTE_NAME}'
)
runner.register(git_fetch)
