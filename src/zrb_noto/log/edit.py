from datetime import datetime

from zrb import Task, python_task, runner
from zrb.helper.task import show_lines

from .._config import IS_AUTO_SYNC
from ..sync import create_sync_noto_task
from ._group import noto_log_group
from ._helper import get_log_file_name, get_pretty_log_lines
from ._input import content_input, date_input


@python_task(
    name="save-file",
    inputs=[
        date_input,
        content_input,
    ],
    retry=0,
)
def save_file(*args, **kwargs):
    date_str = kwargs.get("date")
    content = kwargs.get("content")
    current_time = datetime.strptime(date_str, "%Y-%m-%d")
    file_name = get_log_file_name(current_time)
    with open(file_name, "w") as f:
        f.write(content)


@python_task(
    name="edit",
    group=noto_log_group,
    inputs=[
        date_input,
        content_input,
    ],
    retry=0,
)
def edit_log(*args, **kwargs):
    task: Task = kwargs.get("_task")
    date_str = kwargs.get("date")
    current_time = datetime.strptime(date_str, "%Y-%m-%d")
    file_name = get_log_file_name(current_time)
    show_lines(task, *get_pretty_log_lines(file_name))


if IS_AUTO_SYNC:
    (
        create_sync_noto_task(name="pre-sync")
        >> save_file
        >> create_sync_noto_task(name="post-sync")
        >> edit_log
    )
else:
    save_file >> edit_log

runner.register(edit_log)
