import os

from zrb import CmdTask, runner

from _automate.noto._config import CURRENT_DIR, PROJECT_DIR
from _automate.noto._group import NOTO_GROUP

lint = CmdTask(
    name="lint",
    group=NOTO_GROUP,
    description="Lint code",
    cwd=PROJECT_DIR,
    cmd_path=os.path.join(CURRENT_DIR, "lint.sh"),
)
runner.register(lint)
