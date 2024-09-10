from datetime import datetime

from zrb import Task, python_task, runner
from zrb.helper.task import show_lines

from .._config import IS_AUTO_SYNC
from ..sync import create_sync_noto_task
from ._group import noto_log_group
from ._helper import get_log_file_name, get_pretty_log_lines
from ._input import date_input


@python_task(
    name="list",
    group=noto_log_group,
    inputs=[date_input],
    retry=0,
)
def list_log(*args, **kwargs):
    task: Task = kwargs.get("_task")
    date_str = kwargs.get("date")
    current_time = datetime.strptime(date_str, "%Y-%m-%d")
    file_name = get_log_file_name(current_time)
    show_lines(task, *get_pretty_log_lines(file_name))


if IS_AUTO_SYNC:
    create_sync_noto_task(name="pre-sync") >> list_log
runner.register(list_log)
