from zrb import MultilineInput

from ._config import NOTE_ABS_FILE_PATH
from ._helper import get_note_content

content_input = MultilineInput(
    name="content",
    shortcut="c",
    comment_prefix="<!--",
    comment_suffix="-->",
    extension="md",
    default=lambda m: get_note_content(NOTE_ABS_FILE_PATH),
)
