import os

from zrb import CmdTask, runner

from _automate.noto._config import CURRENT_DIR, PROJECT_DIR
from _automate.noto._group import NOTO_GROUP
from _automate.noto.lint import lint

sync = CmdTask(
    name="sync",
    group=NOTO_GROUP,
    description="Synchronize everything",
    upstreams=[lint],
    cwd=PROJECT_DIR,
    cmd_path=os.path.join(CURRENT_DIR, "sync.sh"),
)
runner.register(sync)
