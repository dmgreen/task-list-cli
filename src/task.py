from datetime import date


class Task:
    def __init__(self, title=None, due_date=None, completed=False):
        self._title = title
        self._due_date = self._normalize_due_date(due_date)
        self.completed = completed

    def create_from_input(self):
        self.title = input("Enter task title: ")
        due_date = input("Enter due date (YYYY-MM-DD, optional): ")
        self.due_date = due_date or None

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, due_date):
        self._due_date = self._normalize_due_date(due_date)

    @property
    def completed(self):
        return self._completed

    @completed.setter
    def completed(self, completed):
        if not isinstance(completed, bool):
            raise TypeError("completed must be a boolean")
        self._completed = completed

    @staticmethod
    def _normalize_due_date(due_date):
        if due_date is None or isinstance(due_date, date):
            return due_date
        if isinstance(due_date, str):
            try:
                return date.fromisoformat(due_date)
            except ValueError as error:
                raise ValueError(
                    "due_date must use YYYY-MM-DD format"
                ) from error
        raise TypeError("due_date must be a date, ISO date string, or None")

    def __str__(self):
        due_date = self._due_date.isoformat() if self._due_date else None
        return (
            f"Task: {self._title} (Due: {due_date}, "
            f"Completed: {self._completed})"
        )
