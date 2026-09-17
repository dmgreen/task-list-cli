from datetime import date
import pytest
from task import Task


def test_task_stores_and_writes_title():
    task = Task("Write tests")

    assert task.title == "Write tests"
    assert str(task) == "Write tests (Due: None, Completed: False)"


def test_task_defaults_metadata():
    task = Task()

    assert task.due_date is None
    assert task.completed is False


def test_task_stores_and_updates_metadata():
    task = Task("Write tests", "2026-09-30", True)

    assert task.due_date == date(2026, 9, 30)
    assert task.completed is True

    task.title = "Review tests"
    task.due_date = date(2026, 10, 1)
    task.completed = False

    assert task.title == "Review tests"
    assert task.due_date == date(2026, 10, 1)
    assert task.completed is False


def test_task_create_from_input_collects_optional_due_date(monkeypatch):
    answers = iter(["Write tests", "2026-09-30"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    task = Task()
    task.create_from_input()

    assert task.title == "Write tests"
    assert task.due_date == date(2026, 9, 30)
    assert task.completed is False


def test_task_create_from_input_allows_blank_due_date(monkeypatch):
    answers = iter(["Write tests", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    task = Task()
    task.create_from_input()

    assert task.due_date is None


def test_task_rejects_invalid_due_date():
    with pytest.raises(ValueError):
        Task(due_date="30-09-2026")

    with pytest.raises(ValueError):
        Task(due_date="2026/09/30")

    with pytest.raises(ValueError):
        Task(due_date="2026-09-31")

    with pytest.raises(ValueError):
        Task(due_date="2026-09-30T12:00:00")


def test_task_rejects_non_boolean_completion():
    with pytest.raises(TypeError):
        Task(completed=1)

    with pytest.raises(TypeError):
        Task(completed=0)
