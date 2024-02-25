from zrb import Parallel, RecurringTask
from .core.start import start
from .core.git.local.check import git_local_check
from .core.git.server.check import git_server_check
from .core.git.push import git_push
from .core.git.pull import git_pull


watch_git_server = RecurringTask(
    name='watch-git-server',
    triggers=[git_server_check],
    task=git_pull
)

watch_git_local = RecurringTask(
    name='watch-git-local',
    triggers=[git_local_check],
    task=git_push
)

Parallel(watch_git_local, watch_git_server) >> start
