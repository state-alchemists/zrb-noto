from typing import Any, Iterable, Optional, Union, Callable
from zrb import runner, Checker, Group, Env, EnvFile, AnyTask, AnyInput
from .._helper import get_current_branch
from ...config import NOTO_GIT_REMOTE_NAME
from ..._group import noto_git_local_group
import subprocess
import os

CURRENT_DIR = os.path.dirname(__file__)
NOTO_DIR = os.path.dirname(os.path.dirname(os.path.dirname(CURRENT_DIR)))


class GitLocalChecker(Checker):

    def __init__(
        self,
        git_remote_name: str,
        name: str = 'check-server',
        group: Optional[Group] = None,
        inputs: Iterable[AnyInput] = [],
        envs: Iterable[Env] = [],
        env_files: Iterable[EnvFile] = [],
        icon: Optional[str] = None,
        color: Optional[str] = None,
        description: str = '',
        upstreams: Iterable[AnyTask] = [],
        checking_interval: Union[int, float] = 0.1,
        progress_interval: Union[int, float] = 30,
        expected_result: bool = True,
        should_execute: Union[bool, str, Callable[..., bool]] = True
    ):
        super().__init__(
            name=name,
            group=group,
            inputs=inputs,
            envs=envs,
            env_files=env_files,
            icon=icon,
            color=color,
            description=description,
            upstreams=upstreams,
            checking_interval=checking_interval,
            progress_interval=progress_interval,
            expected_result=expected_result,
            should_execute=should_execute
        )
        self._git_remote_name = git_remote_name

    async def inspect(self, *args: Any, **kwargs: Any) -> bool:
        # Run the git diff command to compare local and remote branches
        remote_name = self._git_remote_name
        branch = get_current_branch()
        result = subprocess.run(
            [
                'git', 'diff-index', '--quiet', f'{remote_name}/{branch}'
            ],
            cwd=NOTO_DIR,
            stderr=subprocess.STDOUT
        )
        if result.returncode == 1:
            return True
        return False


git_local_check = GitLocalChecker(
    name='check',
    group=noto_git_local_group,
    git_remote_name=NOTO_GIT_REMOTE_NAME,
)
runner.register(git_local_check)
