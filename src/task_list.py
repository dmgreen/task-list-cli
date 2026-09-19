import json
from datetime import date
from pathlib import Path

from task import Task


class TaskFileError(Exception):
    """Raised when a task file cannot be loaded."""


class TaskList:
    def __init__(self, file_path=None):
        self.file_path = Path(file_path if file_path else "tasks.json")
        self._tasks = []
        self._load()

    @property
    def tasks(self):
        return self._tasks

    def sort(self):
        self._tasks.sort(key=lambda t: (t.due_date or date.max, t.title))

    def _load(self):
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
        except (TypeError, ValueError, KeyError) as error:
            raise TaskFileError(f"invalid task record: {error}") from error
        self.sort()

    @staticmethod
    def _task_from_record(record):
        if not isinstance(record, dict):
            raise TypeError("each task must be a JSON object")
        if set(record) != {"title", "due_date", "completed"}:
            raise ValueError(
                "each task must contain title, due_date, and completed"
            )
        return Task(**record)

    def save(self):
        if not self.file_path.exists() and not self._tasks:
            return

        records = [
            {
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

    def add_task(self, task):
        self._tasks.append(task)
        self.sort()

    def get_task(self, task_number):
        if not isinstance(task_number, int) or isinstance(task_number, bool):
            raise TypeError("task number must be an integer")
        if task_number < 1 or task_number > len(self._tasks):
            raise IndexError("task number is out of range")
        return self._tasks[task_number - 1]

    def delete_task(self, task_number):
        task = self.get_task(task_number)
        self._tasks.remove(task)

    def __str__(self):
        if len(self._tasks) == 0:
            return "No tasks available."
        return "\n".join([
            f"{i+1}. {task}" for i, task in enumerate(self._tasks)
        ])
