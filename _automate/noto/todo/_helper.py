import os
import re
from datetime import datetime
from pathlib import Path
from typing import List, Mapping, Optional

from zrb.helper.accessories.color import colored

from _automate.noto._config import TODO_FILE_NAME
from _automate.noto.todo._data import STATUS_ATTRIBUTE_MAP, STATUS_COLOR_MAP, Item


def parse_item(line: str) -> Item:
    line = line.strip()
    # Check for completion
    completed = line.startswith("x ")
    if completed:
        line = line[2:]
    # Check for priority
    priority_match = re.match(r"\(([A-Z])\) ", line)
    priority = None
    if priority_match:
        priority, line = (priority_match.group(1), line[len(priority_match.group(0)) :])
    # Check for completion date
    date_match = re.match(r"(\d{4}-\d{2}-\d{2}) ", line)
    completion_date = None
    if date_match:
        completion_date, line = (
            datetime.strptime(date_match.group(1), "%Y-%m-%d"),
            line[len(date_match.group(0)) :],
        )
    # Check for creation date
    date_match = re.match(r"(\d{4}-\d{2}-\d{2}) ", line)
    creation_date = None
    if date_match:
        creation_date, line = (
            datetime.strptime(date_match.group(1), "%Y-%m-%d"),
            line[len(date_match.group(0)) :],
        )
    elif completion_date is not None:
        creation_date = completion_date
        completion_date = None
    # Extract contexts and projects
    contexts = [context.lstrip("@") for context in re.findall(r"@[\w\-]+", line)]
    projects = [project.lstrip("+") for project in re.findall(r"\+[\w\-]+", line)]
    keyval_match_list = re.findall(r"([\w\-]+):([\w\-]+)", line)
    keyval = {}
    for keyval_match in keyval_match_list:
        keyval[keyval_match[0]] = keyval_match[1]
    # Remove contexts, projects, and keyval from description
    description = re.sub(
        r"(@[\w\-]+|\+[\w\-]+|[\w\-]+:[\w\-]+)", "", line
    ).strip()  # noqa
    return Item(
        description=description,
        old_description=description,
        completed=completed,
        priority=priority,
        completion_date=completion_date,
        creation_date=creation_date,
        contexts=contexts,
        projects=projects,
        keyval=keyval,
    )


def append_item(item: Item, file_name: str = TODO_FILE_NAME) -> str:
    dir_path = Path(os.path.dirname(file_name))
    dir_path.mkdir(parents=True, exist_ok=True)
    items = get_items(file_name=file_name)
    items.append(item)
    _write_items(items, file_name)


def get_items(
    contexts: List[str] = [],
    projects: List[str] = [],
    search: str = "",
    completed: Optional[bool] = None,
    file_name: str = TODO_FILE_NAME,
) -> List[Item]:
    dir_path = Path(os.path.dirname(file_name))
    dir_path.mkdir(parents=True, exist_ok=True)
    if not os.path.isfile(file_name):
        return []
    with open(file_name, "r") as file:
        content = file.read()
    lines = content.split("\n")
    items: List[Item] = []
    filter_by_context = len(contexts) > 0
    filter_by_project = len(projects) > 0
    filter_by_keyword = search != ""
    for line in lines:
        line = line.strip()
        if not line:
            continue
        item = parse_item(line)
        if completed is not None and item.completed != completed:
            continue
        if filter_by_context and not _has_intersection(item.contexts, contexts):
            continue
        if filter_by_project and not _has_intersection(item.projects, projects):
            continue
        if filter_by_keyword and not re.search(search, item.description, re.IGNORECASE):
            continue
        items.append(item)
    return _sort_items(items)


def stop_item(item: Item, file_name: str = TODO_FILE_NAME):
    item.stop()
    replace_item(item, file_name)


def start_item(item: Item, file_name: str = TODO_FILE_NAME):
    item.start()
    replace_item(item, file_name)


def complete_item(item: Item, file_name: str = TODO_FILE_NAME):
    item.complete()
    replace_item(item, file_name)


def delete_item(item: Item, file_name: str = TODO_FILE_NAME):
    items = [
        old_item
        for old_item in get_items(file_name=file_name)
        if old_item.description != item.old_description
    ]
    _write_items(items, file_name)


def replace_item(item: Item, file_name: str = TODO_FILE_NAME):
    items = get_items(file_name=file_name)
    for index, existing_item in enumerate(items):
        if item.old_description == existing_item.description:
            items[index] = item
            break
    _write_items(items, file_name)


def get_existing_contexts(file_name: str = TODO_FILE_NAME) -> List[str]:
    existing_contexts = set()
    items = get_items(file_name=file_name)
    for item in items:
        existing_contexts.update(item.contexts)
    return sorted(list(existing_contexts))


def get_existing_projects(file_name: str = TODO_FILE_NAME) -> List[str]:
    existing_projects = set()
    items = get_items(file_name=file_name)
    for item in items:
        existing_projects.update(item.projects)
    return sorted(list(existing_projects))


def get_pretty_item_lines(items: List[Item]) -> List[str]:
    return [
        "      Completed  Created    Description",
        *[item.as_pretty_str() for item in items],
    ]


def get_kanban_lines(items: List[Item]) -> List[str]:
    status_lines: Mapping[str][List[str]] = {}
    status_max_length: Mapping[str][int] = {}
    status_list = ("NEW", "STOPPED", "STARTED", "COMPLETED")
    for status in status_list:
        status_lines[status] = []
        for item in items:
            if item.get_status() != status:
                continue
            status_lines[status].append(f"* {item.description}")
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
                status_lines[status].append(f"  {project_str}")
            if context_str != "":
                status_lines[status].append(f"  {context_str}")
            if work_duration != "":
                status_lines[status].append(f"  Work: {work_duration}")
            if duration != "":
                status_lines[status].append(f"  Age: {duration}")
            status_lines[status].append("")
        status_max_length[status] = (
            max(len(s) for s in status_lines[status])
            if len(status_lines[status]) > 0
            else len(status)
        )
    lines = []
    # separator
    max_length = sum([status_max_length[status] + 3 for status in status_list])
    separator = "-" * max_length
    # header
    header = ""
    for status in status_list:
        caption = status.ljust(status_max_length[status] + 3)
        header += colored(
            caption,
            color=STATUS_COLOR_MAP[status],
            attrs=STATUS_ATTRIBUTE_MAP[status],
        )
    # add header and separator
    lines.append(separator)
    lines.append(header)
    lines.append(separator)
    # add body
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
    lines.append(separator)
    return lines


def read_keyval_input(keyval_input: str) -> Mapping[str, str]:
    keyval = {}
    for keyval_str in keyval_input.split(","):
        keyval_part = keyval_str.strip().split(":")
        if len(keyval_part) < 2:
            raise Exception(f"Invalid keyval: {keyval_str}")
        keyval[keyval_part[0]] = keyval_part[1]
    return keyval


def _write_items(items: List[Item], file_name: str = TODO_FILE_NAME):
    items = _sort_items(items)
    with open(file_name, "w") as file:
        file.write("\n".join([item.as_str() for item in items]))
        file.write("\n")


def _sort_items(items: List[Item]) -> List[Item]:
    return sorted(
        items,
        key=lambda item: (
            item.completed,
            item.priority,
            sorted(item.projects),
            sorted(item.contexts),
        ),
    )


def _has_intersection(list1: List[str], list2: List[str]):
    set1 = set(list1)
    set2 = set(list2)
    return not set1.isdisjoint(set2)
