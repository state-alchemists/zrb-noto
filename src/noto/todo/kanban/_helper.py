from typing import List, Mapping

from zrb.helper.accessories.color import colored

from .._data import STATUS_ATTRIBUTE_MAP, STATUS_COLOR_MAP, Item


def get_kanban_lines(items: List[Item], screen_width: int) -> List[str]:
    status_lines: Mapping[str][List[str]] = {}
    status_max_length: Mapping[str][int] = {}
    status_list = ("NEW", "STOPPED", "STARTED", "COMPLETED")
    max_width = max(round(screen_width / 4), 15)
    for status in status_list:
        status_lines[status] = []
        for item in items:
            if item.get_status() != status:
                continue
            item_id = item.keyval.get("id", "")
            if item_id != "":
                status_lines[status].append(f"* [{item_id}]"[:max_width])
            status_lines[status].append(f"  {item.description}"[:max_width])
            project_str = " ".join(f"+{project}" for project in sorted(item.projects))
            context_str = " ".join(f"@{context}" for context in sorted(item.contexts))
            work_duration = item.get_work_duration_str()
            duration = item.get_duration_str()
            if (
                project_str != ""
                or context_str != ""
                or work_duration != ""
                or duration != ""
            ):
                status_lines[status].append("")
            if project_str != "":
                status_lines[status].append(f"  {project_str}"[:max_width])
            if context_str != "":
                status_lines[status].append(f"  {context_str}"[:max_width])
            if work_duration != "":
                status_lines[status].append(f"  Work: {work_duration}"[:max_width])
            if duration != "":
                status_lines[status].append(f"  Age: {duration}"[:max_width])
            status_lines[status].append("")
        status_max_length[status] = (
            max(len(s) for s in status_lines[status])
            if len(status_lines[status]) > 0
            else len(status)
        )
    # initiate view
    header = _get_kanban_header(status_list, status_max_length)
    separator = _get_kanban_separator(status_list, status_max_length)
    body = _get_kanban_body(status_list, status_max_length, status_lines)
    return [separator, header, separator, *body, separator]


def _get_kanban_body(
    status_list: List[str],
    status_max_length: Mapping[str, int],
    status_lines: Mapping[str, List[str]],
) -> List[str]:
    lines = []
    index = 0
    while True:
        # check stopping condition
        should_stop = True
        for status in status_list:
            if index < len(status_lines[status]):
                should_stop = False
        if should_stop:
            break
        combined_line = ""
        for status in status_list:
            line_size = len(status_lines[status])
            line = status_lines[status][index] if index < line_size else ""
            line = line.ljust(status_max_length[status] + 3)
            line = colored(line, color=STATUS_COLOR_MAP[status])
            combined_line += line.ljust(status_max_length[status] + 3)
        lines.append(combined_line)
        index += 1
    return lines


def _get_kanban_header(
    status_list: List[str], status_max_length: Mapping[str, int]
) -> str:
    # header
    header = ""
    for status in status_list:
        caption = status.ljust(status_max_length[status] + 3)
        header += colored(
            caption,
            color=STATUS_COLOR_MAP[status],
            attrs=STATUS_ATTRIBUTE_MAP[status],
        )
    return header


def _get_kanban_separator(
    status_list: List[str], status_max_length: Mapping[str, int]
) -> str:
    max_length = sum([status_max_length[status] + 3 for status in status_list])
    return "-" * max_length
