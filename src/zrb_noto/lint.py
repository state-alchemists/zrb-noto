import os

from zrb import CmdTask, runner

from ._env import LOCAL_REPO_DIR_ENV
from ._group import noto_group

_CURRENT_DIR = os.path.dirname(__file__)


lint_noto = CmdTask(
    name="lint",
    group=noto_group,
    description="Lint code",
    envs=[LOCAL_REPO_DIR_ENV],
    cmd_path=os.path.join(_CURRENT_DIR, "lint.sh"),
    should_show_cmd=False,
    should_print_cmd_result=False,
)
runner.register(lint_noto)
