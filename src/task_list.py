import os


class TaskList:
    def __init__(self, file_path=None):
        self.file_path = file_path if file_path else "tasks.json"
        self._tasks = []
        print(f"file_path: {self.file_path}")
        print(f"Exists? {os.path.exists(self.file_path)}")

    @property
    def tasks(self):
        return self._tasks

    def add_task(self, task):
        self._tasks.append(task)

    def __str__(self):
        if len(self._tasks) == 0:
            return "No tasks available."
        return "\n".join([
            f"{i+1}. {task}" for i, task in enumerate(self._tasks)
        ])
