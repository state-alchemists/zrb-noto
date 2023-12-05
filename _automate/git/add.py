from zrb import runner, CmdTask
from .._group import noto_git_group
from .fetch import git_fetch
import os

CURRENT_DIR = os.path.dirname(__file__)
NOTO_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))

git_add = CmdTask(
    name='add',
    group=noto_git_group,
    upstreams=[git_fetch],
    cwd=NOTO_DIR,
    cmd='git add . -A'
)
runner.register(git_add)
