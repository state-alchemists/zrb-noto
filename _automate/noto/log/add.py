from datetime import datetime

from zrb import StrInput, Task, python_task, runner
from zrb.helper.python_task import show_lines

from _automate.noto._config import CURRENT_TIME
from _automate.noto.log._group import LOG_GROUP
from _automate.noto.log._helper import append_log, get_log, get_log_file_name


@python_task(
    name="add",
    group=LOG_GROUP,
    inputs=[
        StrInput(
            name="date",
            prompt="Date (Y-m-d)",
            default=CURRENT_TIME.strftime("%Y-%m-%d"),
        ),
        StrInput(
            name="time", prompt="Time (H:M)", default=CURRENT_TIME.strftime("%H:%M")
        ),
        StrInput(
            name="content",
            prompt="Content",
            default="",
        ),
    ],
)
def add(*args, **kwargs):
    task: Task = kwargs.get("_task")
    date_str = kwargs.get("date")
    time_str = kwargs.get("time")
    content = kwargs.get("content")
    current_time = datetime.strptime(date_str, "%Y-%m-%d")
    file_name = get_log_file_name(current_time)
    append_log(file_name, f"- {time_str}: {content}")
    log_str = get_log(file_name)
    logs = log_str.split("\n")
    show_lines(task, *logs)


runner.register(add)
