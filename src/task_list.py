import os
from datetime import date


class TaskList:
    def __init__(self, file_path=None):
        self.file_path = file_path if file_path else "tasks.json"
        self._tasks = []
        print(f"file_path: {self.file_path}")
        print(f"Exists? {os.path.exists(self.file_path)}")

    @property
    def tasks(self):
        return self._tasks

    def sort(self):
        self._tasks.sort(key=lambda t: (t.due_date or date.max, t.title))

    def add_task(self, task):
        self._tasks.append(task)
        self.sort()

    def get_task(self, task_number):
        if not isinstance(task_number, int) or isinstance(task_number, bool):
            raise TypeError("task number must be an integer")
        if task_number < 1 or task_number > len(self._tasks):
            raise IndexError("task number is out of range")
        return self._tasks[task_number - 1]

    def __str__(self):
        if len(self._tasks) == 0:
            return "No tasks available."
        return "\n".join([
            f"{i+1}. {task}" for i, task in enumerate(self._tasks)
        ])
