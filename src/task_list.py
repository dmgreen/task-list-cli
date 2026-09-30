import json
from datetime import date
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union, cast

from platformdirs import user_data_dir

from task import Task


def default_task_file() -> Path:
    """Return the platform-specific default task file path."""
    return Path(user_data_dir("task-list-cli")) / "tasks.json"


class TaskFileError(Exception):
    """Raised when a task file cannot be loaded."""


class TaskList:
    def __init__(self, file_path: Optional[Union[str, Path]] = None) -> None:
        self.file_path = (
            Path(file_path) if file_path is not None else default_task_file()
        )
        self._tasks: List[Task] = []
        self._load()

    @property
    def tasks(self) -> List[Task]:
        return self._tasks

    def sort(self) -> None:
        self._tasks.sort(key=lambda t: (t.due_date or date.max, t.title))

    def _load(self) -> None:
        if not self.file_path.exists():
            return

        try:
            with self.file_path.open(encoding="utf-8") as task_file:
                records = json.load(task_file)
        except (OSError, json.JSONDecodeError) as error:
            message = f"could not load {self.file_path}: {error}"
            raise TaskFileError(message) from error

        if not isinstance(records, list):
            raise TaskFileError("task file must contain a JSON array")

        try:
            self._tasks = [
                self._task_from_record(record) for record in records
            ]
            task_ids = [task.id for task in self._tasks]
            if len(task_ids) != len(set(task_ids)):
                raise ValueError("task IDs must be unique")
        except (TypeError, ValueError, KeyError) as error:
            raise TaskFileError(f"invalid task record: {error}") from error
        self.sort()

    @staticmethod
    def _task_from_record(record: object) -> Task:
        if not isinstance(record, dict):
            raise TypeError("each task must be a JSON object")
        record = cast(Dict[str, Any], record)
        legacy_fields = {"title", "due_date", "completed"}
        if set(record) not in (legacy_fields, legacy_fields | {"id"}):
            raise ValueError(
                "each task must contain title, due_date, and completed, "
                "and may contain id"
            )
        values = dict(record)
        if "id" in values:
            values["task_id"] = values.pop("id")
        return Task(**values)

    def save(self) -> None:
        if not self.file_path.exists() and not self._tasks:
            return

        records = [
            {
                "id": task.id,
                "title": task.title,
                "due_date": (
                    task.due_date.isoformat() if task.due_date else None
                ),
                "completed": task.completed,
            }
            for task in self._tasks
        ]
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            with self.file_path.open("w", encoding="utf-8") as task_file:
                json.dump(records, task_file, indent=2)
                task_file.write("\n")
        except OSError as error:
            message = f"could not save {self.file_path}: {error}"
            raise TaskFileError(message) from error

    def add_task(self, task: Task) -> None:
        self._tasks.append(task)
        self.sort()

    def get_task(self, task_number: int) -> Task:
        if not isinstance(task_number, int) or isinstance(task_number, bool):
            raise TypeError("task number must be an integer")
        if task_number < 1 or task_number > len(self._tasks):
            raise IndexError("task number is out of range")
        return self._tasks[task_number - 1]

    def delete_task(self, task_number: int) -> None:
        task = self.get_task(task_number)
        self._tasks.remove(task)

    def get_task_by_id(self, task_id: str) -> Task:
        for task in self._tasks:
            if task.id == task_id:
                return task
        raise KeyError(f"task {task_id} was not found")

    def delete_task_by_id(self, task_id: str) -> None:
        self._tasks.remove(self.get_task_by_id(task_id))

    def to_str(
            self,
            filter_func: Optional[Callable[[Task], bool]] = None) -> str:
        output = self._tasks
        if filter_func is not None:
            output = list(filter(filter_func, output))

        if len(output) == 0:
            return "No tasks available."
        return "\n".join([
            f"{i+1}. {task}" for i, task in enumerate(output)
        ])

    def __str__(self) -> str:
        return self.to_str()
