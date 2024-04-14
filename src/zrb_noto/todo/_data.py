import re
from datetime import datetime
from typing import List, Mapping, Optional

from zrb.helper.accessories.color import colored
from zrb.helper.accessories.name import get_random_name

from .._config import CURRENT_TIME
from .._helper import get_screen_width

SCREEN_WIDTH = get_screen_width()

STATUS_ICON_MAP = {
    "NEW": "✨",
    "STARTED": "🏃",
    "STOPPED": "🌴",
    "COMPLETED": "🏆",
}

STATUS_COLOR_MAP = {
    "NEW": "white",
    "STARTED": "light_cyan",
    "STOPPED": "light_red",
    "COMPLETED": "light_green",
}

STATUS_ATTRIBUTE_MAP = {
    "NEW": [],
    "STARTED": ["bold"],
    "STOPPED": ["bold"],
    "COMPLETED": [],
}


class Item:
    def __init__(
        self,
        description: str,
        old_description: Optional[str] = None,
        completed: bool = False,
        priority: Optional[str] = None,
        completion_date: Optional[datetime] = None,
        creation_date: Optional[datetime] = None,
        contexts: List[str] = [],
        projects: List[str] = [],
        keyval: Mapping[str, str] = {},
    ):
        self.completed = completed
        self.priority = priority
        self.completion_date = completion_date
        self.creation_date = creation_date
        self.description = description
        self.old_description = old_description
        self.contexts = contexts
        self.projects = projects
        self.keyval = keyval
        if "id" not in self.keyval:
            self.keyval["id"] = get_random_name()

    def match(
        self,
        contexts: List[str] = [],
        projects: List[str] = [],
        search: str = "",
        completed: Optional[bool] = None,
    ):
        filter_by_context = len(contexts) > 0
        filter_by_project = len(projects) > 0
        filter_by_keyword = search != "" and search is not None
        if completed is not None and self.completed != completed:
            return False
        if filter_by_context and not _has_intersection(self.contexts, contexts):
            return False
        if filter_by_project and not _has_intersection(self.projects, projects):
            return False
        if filter_by_keyword:
            if re.search(search, self.description, re.IGNORECASE):
                return True
            if "id" in self.keyval:
                if re.search(search, self.keyval.get("id"), re.IGNORECASE):
                    return True
            return False
        return True

    def set_keyval(self, new_keyval: Mapping[str, str]):
        old_keyval = self.keyval
        for key in (
            "id",
            "createdAt",
            "firstCreatedAt",
            "lastStartedAt",
            "status",
            "workDuration",
        ):
            if key in old_keyval and key not in new_keyval:
                new_keyval[key] = old_keyval[key]
        self.keyval = new_keyval

    def start(self):
        timestamp = round(CURRENT_TIME.timestamp())
        self.keyval["lastStartedAt"] = timestamp
        if "firstStartedAt" not in self.keyval:
            self.keyval["firstStartedAt"] = timestamp
        if "workDuration" not in self.keyval:
            self.keyval["workDuration"] = 0
        self.keyval["status"] = "started"

    def stop(self):
        self._stop()
        self.keyval["status"] = "stopped"

    def complete(self):
        self._stop()
        self.completed = True
        self.completion_date = CURRENT_TIME
        self.keyval["status"] = "completed"

    def _stop(self):
        timestamp = round(CURRENT_TIME.timestamp())
        if self.get_status() != "STARTED":
            return
        self.keyval["lastStoppedAt"] = timestamp
        last_started_at = int(self.keyval.get("lastStartedAt", str(timestamp)))
        previous_duration = int(self.keyval.get("workDuration", "0"))
        self.keyval["workDuration"] = previous_duration + (timestamp - last_started_at)

    def as_pretty_str(self, screen_width: int = SCREEN_WIDTH) -> str:
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
        # project
        project_str = " ".join([f"+{project}" for project in sorted(self.projects)])
        if project_str != "":
            project_str = colored(f" {project_str}", color="yellow")
        # context
        context_str = " ".join([f"@{context}" for context in sorted(self.contexts)])
        if context_str != "":
            context_str = colored(f" {context_str}", color="blue")
        # keyval
        keyval_str = " ".join(
            f"{key}:{val}" for key, val in self._get_published_keyval().items()
        )
        if keyval_str != "":
            keyval_str = colored(f" {keyval_str}", color="magenta")
        # id
        id = self.keyval.get("id")
        id_str = colored(f"[{id}]", attrs=["dark"])
        # description
        description_str = self._get_colored_description()
        # Status string
        status_icon = self._get_status_icon()
        # work duration
        work_duration_str = self.get_work_duration_str()
        if work_duration_str != "":
            work_duration_str = colored(f" (🔨 {work_duration_str})", color="cyan")
        # duration
        duration_str = self.get_duration_str()
        if duration_str != "":
            duration_str = colored(f" (🌱 {duration_str})", color="green")
        # small screen
        if screen_width <= 80:
            return f"{completed_str} {priority_str} {status_icon} {id_str} {description_str}{project_str}{context_str}{keyval_str}{work_duration_str}"  # noqa
        # normal screen
        return f"{completed_str} {priority_str} {completion_date_str} {creation_date_str} {status_icon} {id_str} {description_str}{project_str}{context_str}{keyval_str}{duration_str}{work_duration_str}"  # noqa

    def _get_published_keyval(self):
        return {
            key: val
            for key, val in self.keyval.items()
            if key
            not in [
                "id",
                "createdAt",
                "firstStartedAt",
                "lastStartedAt",
                "lastStoppedAt",
                "status",
                "workDuration",
            ]
        }

    def _get_colored_description(self):
        status = self.get_status()
        description_str = self.description
        return colored(
            description_str,
            color=STATUS_COLOR_MAP.get(status),
            attrs=STATUS_ATTRIBUTE_MAP.get(status),
        )

    def _get_status_icon(self):
        status = self.get_status()
        status_str = STATUS_ICON_MAP.get(status)
        return status_str

    def get_id(self):
        return self.keyval.get("id", "xxxx-xxxx-xxxx")

    def get_status(self):
        if self.completed:
            return "COMPLETED"
        status = self.keyval.get("status", "new").upper()
        if status not in STATUS_ICON_MAP:
            status = "NEW"
        return status

    def get_work_duration_str(self):
        status = self.keyval.get("status", "new").upper()
        # get working duration
        work_duration = int(self.keyval.get("workDuration", "0"))
        if status == "STARTED":
            last_started_at = int(self.keyval.get("lastStartedAt", "-1"))
            if last_started_at != -1:
                work_duration += round(CURRENT_TIME.timestamp() - last_started_at)
        if work_duration == 0:
            return ""
        return _seconds_to_human_time(work_duration)

    def get_duration_str(self):
        created_at = int(self.keyval.get("createdAt", "-1"))
        if created_at == -1 and self.creation_date is not None:
            created_at = self.creation_date.timestamp()
        duration = round(CURRENT_TIME.timestamp() - created_at)
        if duration == 0:
            return ""
        return _seconds_to_human_time(duration)

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
        # project
        project_str = " ".join([f"+{project}" for project in sorted(self.projects)])
        if project_str != "":
            project_str = f" {project_str}"
        # context
        context_str = " ".join([f"@{context}" for context in sorted(self.contexts)])
        if context_str != "":
            context_str = f" {context_str}"
        # keyval
        keyval_str = " ".join(f"{key}:{val}" for key, val in self.keyval.items())
        if keyval_str != "":
            keyval_str = f" {keyval_str}"
        return f"{completed_str}{priority_str}{completion_date_str}{creation_date_str}{self.description}{project_str}{context_str}{keyval_str}"  # noqa


def _has_intersection(list1: List[str], list2: List[str]):
    set1 = set(list1)
    set2 = set(list2)
    return not set1.isdisjoint(set2)


def _seconds_to_human_time(seconds: int):
    years = seconds // 31536000
    seconds %= 31536000
    months = seconds // 2592000
    seconds %= 2592000
    days = seconds // 86400
    seconds %= 86400
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    if years > 0:
        return f"{years}y {months}m {days}d"
    if months > 0:
        return f"{months}m {days}d {hours}h"
    if days > 0:
        return f"{days}d {hours}h"
    if hours > 0:
        return f"{hours}h {minutes} min"
    if minutes == 0:
        return ""
    return f"{minutes} min"
