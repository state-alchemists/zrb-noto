from zrb import runner, python_task, Task
from .core._group import noto_group
from .core import git
assert git


@python_task(
    name='start',
    icon='🤖',
    color='green',
    group=noto_group,
    description='Start noto monitoring system',
    runner=runner
)
def start(*args, **kwargs):
    task: Task = kwargs.get('_task')
    task.print_out('Noto monitoring started')
