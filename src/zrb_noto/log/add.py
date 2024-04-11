from zrb import StrInput, Task, python_task, runner
from zrb.helper.task import show_lines

from ..sync import create_sync_noto_task
from ._group import noto_log_group
from ._helper import append_log_item, get_pretty_log_lines


@python_task(
    name="add-item",
    inputs=[
        StrInput(
            name="text",
            shortcut="t",
            prompt="Text",
            default="",
        ),
    ],
    retry=0,
)
def add_item(*args, **kwargs):
    text = kwargs.get("text")
    append_log_item(text)


@python_task(
    name="add",
    group=noto_log_group,
    inputs=[
        StrInput(
            name="text",
            shortcut="t",
            prompt="Text",
            default="",
        ),
    ],
    retry=0,
)
def add_log(*args, **kwargs):
    task: Task = kwargs.get("_task")
    show_lines(task, *get_pretty_log_lines())


create_sync_noto_task() >> add_item >> create_sync_noto_task() >> add_log
runner.register(add_log)
