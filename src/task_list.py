import os

class task_list:
    def __init__(self, file_path = None):
        self.file_path = file_path if file_path else "tasks.json"

        print(f"File path - {self.file_path} - {'does' if os.path.exists(self.file_path) else 'does not'} exist.")
        self._tasks = []

    @property
    def tasks(self):
        return self._tasks