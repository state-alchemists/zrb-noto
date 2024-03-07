import os
import re
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from zrb.helper.accessories.color import colored

from _automate.noto._config import TODO_FILE_NAME


class Item:
    def __init__(
        self,
        description: str,
        completed: bool = False,
        priority: Optional[str] = None,
        creation_date: Optional[datetime] = None,
        contexts: List[str] = [],
        projects: List[str] = [],
    ):
        self.completed = completed
        self.priority = priority
        self.creation_date = creation_date
        self.description = description
        self.contexts = contexts
        self.projects = projects

    def as_str(self, show_empty=False, show_color=False) -> str:
        # complete
        empty_completed_str = " " if show_empty else ""
        completed_str = "x" if self.completed else empty_completed_str
        if show_color:
            completed_str = colored(completed_str, color="cyan")
        # priority
        empty_priority_str = "( )" if show_empty else ""
        priority_str = (
            empty_priority_str if self.priority is None else f"({self.priority})"
        )
        if show_color:
            priority_str = colored(priority_str, color="magenta")
        # creation date
        empty_creation_date_str = "                " if show_empty else ""
        creation_date_str = (
            empty_creation_date_str
            if self.creation_date is None
            else self.creation_date.strftime("%Y-%m-%d %H:%M")
        )
        if show_color:
            creation_date_str = colored(creation_date_str, color="green")
        context_str = " ".join([f"@{context}" for context in self.contexts])
        if show_color:
            context_str = colored(context_str, color="blue")
        project_str = " ".join([f"+{project}" for project in self.projects])
        if show_color:
            project_str = colored(project_str, color="yellow")
        return f"{completed_str} {priority_str} {creation_date_str} {self.description} {project_str} {context_str}"  # noqa


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
    # Check for creation date
    date_match = re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) ", line)
    creation_date = None
    if date_match:
        creation_date, line = (
            datetime.strptime(date_match.group(1), "%Y-%m-%d %H:%M"),
            line[len(date_match.group(0)) :],
        )
    # Extract contexts and projects
    contexts = [context.lstrip("@") for context in re.findall(r"@\w+", line)]
    projects = [project.lstrip("+") for project in re.findall(r"\+\w+", line)]
    # Remove contexts and projects from description
    description = re.sub(r"(@\w+|\+\w+)", "", line).strip()  # noqa
    return Item(
        description=description,
        completed=completed,
        priority=priority,
        creation_date=creation_date,
        contexts=contexts,
        projects=projects,
    )


def append_item(item: Item, file_name: str = TODO_FILE_NAME) -> str:
    dir_path = Path(os.path.dirname(file_name))
    dir_path.mkdir(parents=True, exist_ok=True)
    with open(file_name, "a") as file:
        file.write(f"{item.as_str()}\n")


def get_items(file_name: str = TODO_FILE_NAME) -> str:
    dir_path = Path(os.path.dirname(file_name))
    dir_path.mkdir(parents=True, exist_ok=True)
    with open(file_name, "r") as file:
        content = file.read()
        lines = content.split("\n")
        items: List[Item] = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            items.append(parse_item(line))
        return items
