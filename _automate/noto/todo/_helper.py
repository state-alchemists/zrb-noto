import os
import re
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from zrb.helper.accessories.color import colored

from _automate.noto._config import CURRENT_TIME, TODO_FILE_NAME


class Item:
    def __init__(
        self,
        description: str,
        completed: bool = False,
        priority: Optional[str] = None,
        completion_date: Optional[datetime] = None,
        creation_date: Optional[datetime] = None,
        contexts: List[str] = [],
        projects: List[str] = [],
    ):
        self.completed = completed
        self.priority = priority
        self.completion_date = completion_date
        self.creation_date = creation_date
        self.description = description
        self.contexts = contexts
        self.projects = projects

    def as_pretty_str(self) -> str:
        # complete
        completed_str = "x" if self.completed else " "
        completed_str = colored(completed_str, color="cyan")
        # priority
        priority_str = "( )" if self.priority is None else f"({self.priority})"
        priority_str = colored(priority_str, color="magenta")
        # completion date
        completion_date_str = (
            " " * 10
            if self.completion_date is None
            else self.completion_date.strftime("%Y-%m-%d")
        )
        completion_date_str = colored(completion_date_str, color="yellow")
        # creation date
        creation_date_str = (
            " " * 10
            if self.creation_date is None
            else self.creation_date.strftime("%Y-%m-%d")
        )
        creation_date_str = colored(creation_date_str, color="green")
        # context
        context_str = " ".join([f"@{context}" for context in sorted(self.contexts)])
        context_str = colored(context_str, color="blue")
        # project
        project_str = " ".join([f"+{project}" for project in sorted(self.projects)])
        project_str = colored(project_str, color="yellow")
        return f"{completed_str} {priority_str} {completion_date_str} {creation_date_str} {self.description} {project_str} {context_str}"  # noqa

    def as_str(self) -> str:
        # complete
        completed_str = "x " if self.completed else ""
        # priority
        priority_str = "" if self.priority is None else f"({self.priority}) "
        # completion date
        completion_date_str = (
            ""
            if self.completion_date is None
            else self.completion_date.strftime("%Y-%m-%d") + " "
        )
        # creation date
        creation_date_str = (
            ""
            if self.creation_date is None
            else self.creation_date.strftime("%Y-%m-%d") + " "
        )
        # context
        context_str = " ".join([f"@{context}" for context in sorted(self.contexts)])
        # project
        project_str = " ".join([f"+{project}" for project in sorted(self.projects)])
        return f"{completed_str}{priority_str}{completion_date_str}{creation_date_str}{self.description} {project_str} {context_str}"  # noqa


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
    contexts = [context.lstrip("@") for context in re.findall(r"@\w+", line)]
    projects = [project.lstrip("+") for project in re.findall(r"\+\w+", line)]
    # Remove contexts and projects from description
    description = re.sub(r"(@\w+|\+\w+)", "", line).strip()  # noqa
    return Item(
        description=description,
        completed=completed,
        priority=priority,
        completion_date=completion_date,
        creation_date=creation_date,
        contexts=contexts,
        projects=projects,
    )


def append_item(item: Item, file_name: str = TODO_FILE_NAME) -> str:
    dir_path = Path(os.path.dirname(file_name))
    dir_path.mkdir(parents=True, exist_ok=True)
    with open(file_name, "a") as file:
        file.write(f"{item.as_str()}\n")


def get_items(
    contexts: List[str] = [],
    projects: List[str] = [],
    search: str = "",
    completed: Optional[bool] = None,
    file_name: str = TODO_FILE_NAME,
) -> List[Item]:
    dir_path = Path(os.path.dirname(file_name))
    dir_path.mkdir(parents=True, exist_ok=True)
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
    return sort_items(items)


def sort_items(items: List[Item]) -> List[Item]:
    return sorted(
        items,
        key=lambda item: (
            item.completed,
            item.priority,
            sorted(item.projects),
            sorted(item.contexts),
        ),
    )


def complete_item(item: Item, file_name: str = TODO_FILE_NAME):
    items = get_items(file_name=file_name)
    for index, existing_item in enumerate(items):
        if item.description == existing_item.description:
            items[index].completed = True
            items[index].completion_date = CURRENT_TIME
            break
    items = sort_items(items)
    with open(file_name, "w") as file:
        file.write("\n".join([item.as_str() for item in items]))
        file.write("\n")


def get_existing_contexts() -> List[str]:
    existing_contexts = set()
    items = get_items()
    for item in items:
        existing_contexts.update(item.contexts)
    return sorted(list(existing_contexts))


def get_existing_projects() -> List[str]:
    existing_projects = set()
    items = get_items()
    for item in items:
        existing_projects.update(item.projects)
    return sorted(list(existing_projects))


def get_pretty_lines(items: List[Item]):
    return [
        "      Completed  Created    Description",
        *[item.as_pretty_str() for item in items],
    ]


def _has_intersection(list1: List[str], list2: List[str]):
    set1 = set(list1)
    set2 = set(list2)
    return not set1.isdisjoint(set2)
