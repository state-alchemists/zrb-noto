from zrb import StrInput, Task, python_task, runner
from zrb.helper.python_task import show_lines

from _daily.noto.log._group import LOG_GROUP
from _daily.noto.log._helper import append_log, get_log_lines


@python_task(
    name="add",
    group=LOG_GROUP,
    inputs=[
        StrInput(
            name="text",
            prompt="Text",
            default="",
        ),
    ],
    retry=0,
)
def add(*args, **kwargs):
    task: Task = kwargs.get("_task")
    text = kwargs.get("text")
    append_log(text)
    show_lines(task, *get_log_lines())


runner.register(add)
