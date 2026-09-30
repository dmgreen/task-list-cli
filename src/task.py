from datetime import date
from typing import Optional, Union, overload
from uuid import UUID, uuid4

_UNSET = object()


class Task:
    def __init__(
        self,
        title: Optional[str] = None,
        due_date: Optional[Union[date, str]] = None,
        completed: bool = False,
        task_id: Optional[str] = None,
    ) -> None:
        self._id = self._normalize_id(task_id)
        self._title = self._normalize_title(title)
        self._due_date = self._normalize_due_date(due_date)
        self.completed = completed

    @overload
    def update(
        self,
        *,
        title: str = ...,
        due_date: Optional[Union[date, str]] = ...,
        completed: bool = ...,
    ) -> None:
        ...

    def update(
        self,
        *,
        title: object = _UNSET,
        due_date: object = _UNSET,
        completed: object = _UNSET,
    ) -> None:
        if title is not _UNSET:
            title = self._normalize_title(title)
        if due_date is not _UNSET:
            due_date = self._normalize_due_date(due_date)
        if completed is not _UNSET and not isinstance(completed, bool):
            raise TypeError("completed must be a boolean")

        if title is not _UNSET:
            self.title = title
        if due_date is not _UNSET:
            self.due_date = due_date
        if completed is not _UNSET:
            self.completed = completed

    @property
    def title(self) -> str:
        return self._title

    @property
    def id(self) -> str:
        return self._id

    @title.setter
    def title(self, title: Optional[str]) -> None:
        self._title = self._normalize_title(title)

    @property
    def due_date(self) -> Optional[date]:
        return self._due_date

    @due_date.setter
    def due_date(self, due_date: Optional[Union[date, str]]) -> None:
        self._due_date = self._normalize_due_date(due_date)

    @property
    def completed(self) -> bool:
        return self._completed

    @completed.setter
    def completed(self, completed: bool) -> None:
        if not isinstance(completed, bool):
            raise TypeError("completed must be a boolean")
        self._completed = completed

    @staticmethod
    def _normalize_title(title: object) -> str:
        if not isinstance(title, str):
            raise TypeError("title must be a string")
        title = title.strip()
        if not title:
            raise ValueError("Task title is required")
        return title

    @staticmethod
    def _normalize_id(task_id: Optional[str]) -> str:
        if task_id is None:
            return str(uuid4())
        if not isinstance(task_id, str):
            raise TypeError("task id must be a string")
        try:
            return str(UUID(task_id))
        except ValueError as error:
            raise ValueError("task id must be a valid UUID") from error

    @staticmethod
    def _normalize_due_date(
        due_date: object,
    ) -> Optional[date]:
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

    def __str__(self) -> str:
        due_date = self._due_date.isoformat() if self._due_date else None
        return (
            f"{self._title} (Due: {due_date}, "
            f"Completed: {self._completed})"
        )
