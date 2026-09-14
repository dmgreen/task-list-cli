class Task:
    def __init__(self, title=None):
        self._title = title

    def create_from_input(self):
        self._title = input("Enter task title: ")

    @property
    def title(self):
        return self._title

    def __str__(self):
        return f"Task: {self._title}"
