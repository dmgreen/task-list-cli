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