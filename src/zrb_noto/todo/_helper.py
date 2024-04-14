import os
import re
from datetime import datetime
from pathlib import Path
from typing import List, Mapping, Optional

from .._config import TODO_ABS_FILE_PATH
from .._helper import get_screen_width
from ._data import Item

SCREEN_WIDTH = get_screen_width()


def parse_todo_item(line: str) -> Item:
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
    description = re.sub(r"(@[\w\-]+|\+[\w\-]+|[\w\-]+:[\w\-]+)", "", line).strip()
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


def append_todo_item(item: Item, file_name: str = TODO_ABS_FILE_PATH) -> str:
    dir_path = Path(os.path.dirname(file_name))
    dir_path.mkdir(parents=True, exist_ok=True)
    items = get_todo_items(file_name=file_name)
    items.append(item)
    save_items(items, file_name)


def get_todo_items(
    contexts: List[str] = [],
    projects: List[str] = [],
    search: str = "",
    completed: Optional[bool] = None,
    file_name: str = TODO_ABS_FILE_PATH,
) -> List[Item]:
    dir_path = Path(os.path.dirname(file_name))
    dir_path.mkdir(parents=True, exist_ok=True)
    if not os.path.isfile(file_name):
        return []
    with open(file_name, "r") as file:
        content = file.read()
    lines = content.split("\n")
    items: List[Item] = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        item = parse_todo_item(line)
        if item.match(
            contexts=contexts, projects=projects, search=search, completed=completed
        ):
            items.append(item)
    return _sort_items(items)


def stop_todo_item(item: Item, file_name: str = TODO_ABS_FILE_PATH):
    item.stop()
    replace_todo_item(item, file_name)


def start_todo_item(item: Item, file_name: str = TODO_ABS_FILE_PATH):
    item.start()
    replace_todo_item(item, file_name)


def complete_todo_item(item: Item, file_name: str = TODO_ABS_FILE_PATH):
    item.complete()
    replace_todo_item(item, file_name)


def delete_todo_item(item: Item, file_name: str = TODO_ABS_FILE_PATH):
    items = [
        old_item
        for old_item in get_todo_items(file_name=file_name)
        if old_item.description != item.old_description
    ]
    save_items(items, file_name)


def replace_todo_item(item: Item, file_name: str = TODO_ABS_FILE_PATH):
    items = get_todo_items(file_name=file_name)
    for index, existing_item in enumerate(items):
        if item.old_description == existing_item.description:
            items[index] = item
            break
    save_items(items, file_name)


def get_existing_todo_contexts(file_name: str = TODO_ABS_FILE_PATH) -> List[str]:
    existing_contexts = set()
    items = get_todo_items(file_name=file_name)
    for item in items:
        existing_contexts.update(item.contexts)
    return sorted(list(existing_contexts))


def get_existing_todo_projects(file_name: str = TODO_ABS_FILE_PATH) -> List[str]:
    existing_projects = set()
    items = get_todo_items(file_name=file_name)
    for item in items:
        existing_projects.update(item.projects)
    return sorted(list(existing_projects))


def get_pretty_todo_item_lines(
    items: List[Item], screen_width: int = SCREEN_WIDTH
) -> List[str]:
    if screen_width <= 80:
        return [
            "      Description",
            *[item.as_pretty_str(screen_width=screen_width) for item in items],
        ]
    return [
        "      Completed  Created    Description",
        *[item.as_pretty_str(screen_width=screen_width) for item in items],
    ]


def read_keyval_input(keyval_input: str) -> Mapping[str, str]:
    keyval = {}
    for keyval_str in keyval_input.split(","):
        keyval_part = keyval_str.strip().split(":")
        if len(keyval_part) < 2:
            raise Exception(f"Invalid keyval: {keyval_str}")
        keyval[keyval_part[0]] = keyval_part[1]
    return keyval


def save_items(items: List[Item], file_name: str = TODO_ABS_FILE_PATH):
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
