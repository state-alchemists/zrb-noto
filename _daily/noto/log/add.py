from zrb import StrInput, Task, python_task, runner
from zrb.helper.python_task import show_lines

from _daily.noto._helper import sync_noto
from _daily.noto.log._group import LOG_GROUP
from _daily.noto.log._helper import append_log, get_pretty_log_lines


@python_task(
    name="add",
    group=LOG_GROUP,
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
def add(*args, **kwargs):
    task: Task = kwargs.get("_task")
    sync_noto(task)
    text = kwargs.get("text")
    append_log(text)
    sync_noto(task)
    show_lines(task, *get_pretty_log_lines())


runner.register(add)
