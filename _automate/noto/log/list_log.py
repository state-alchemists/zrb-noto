from datetime import datetime

from zrb import StrInput, Task, python_task, runner
from zrb.helper.python_task import show_lines

from _automate.noto._config import CURRENT_TIME
from _automate.noto.log._group import LOG_GROUP
from _automate.noto.log._helper import get_log_file_name, get_pretty_log_lines


@python_task(
    name="list",
    group=LOG_GROUP,
    inputs=[
        StrInput(
            name="date",
            prompt="Date (Y-m-d)",
            default=CURRENT_TIME.strftime("%Y-%m-%d"),
        ),
    ],
    retry=0,
)
def list_log(*args, **kwargs):
    task: Task = kwargs.get("_task")
    date_str = kwargs.get("date")
    current_time = datetime.strptime(date_str, "%Y-%m-%d")
    file_name = get_log_file_name(current_time)
    show_lines(task, *get_pretty_log_lines(file_name))


runner.register(list_log)
