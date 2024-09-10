from zrb import Task, python_task, runner
from zrb.helper.task import show_lines

from ._config import IS_AUTO_SYNC, NOTE_ABS_FILE_PATH
from ._helper import get_note_content
from ._input import content_input
from .sync import create_sync_noto_task


@python_task(
    name="save-file",
    inputs=[content_input],
    retry=0,
)
def save_file(*args, **kwargs):
    content = kwargs.get("content")
    with open(NOTE_ABS_FILE_PATH, "w") as f:
        f.write(content)


@python_task(
    name="note",
    inputs=[content_input],
    retry=0,
)
def note(*args, **kwargs):
    task: Task = kwargs.get("_task")
    show_lines(task, *get_note_content(NOTE_ABS_FILE_PATH).split("\n"))


if IS_AUTO_SYNC:
    (
        create_sync_noto_task(name="pre-sync")
        >> save_file
        >> create_sync_noto_task(name="post-sync")
        >> note
    )
else:
    save_file >> note

runner.register(note)
