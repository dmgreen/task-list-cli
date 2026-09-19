from datetime import date

import pytest

from task import Task


def test_task_stores_and_writes_title():
    task = Task("Write tests")

    assert task.title == "Write tests"
    assert str(task) == "Write tests (Due: None, Completed: False)"


def test_task_defaults_metadata():
    task = Task("Write tests")

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


def test_task_rejects_blank_title():
    with pytest.raises(ValueError):
        Task(" ")


def test_task_requires_title():
    with pytest.raises(TypeError):
        Task()


def test_task_strips_title():
    task = Task("  Write tests  ")

    assert task.title == "Write tests"


def test_task_update_changes_each_property():
    task = Task("Write tests", "2026-09-30", False)

    task.update(title="Review tests", due_date="2026-10-01", completed=True)

    assert task.title == "Review tests"
    assert task.due_date == date(2026, 10, 1)
    assert task.completed is True


def test_task_update_can_clear_due_date():
    task = Task("Write tests", "2026-09-30", False)

    task.update(due_date=None)

    assert task.due_date is None


def test_task_update_requires_title_if_provided():
    task = Task("Write tests", "2026-09-30", False)

    with pytest.raises(ValueError):
        task.update(title=" ")

    assert task.title == "Write tests"


def test_task_update_is_atomic_when_validation_fails():
    task = Task("Write tests", "2026-09-30", False)

    with pytest.raises(ValueError):
        task.update(title="Review tests", due_date="2026-09-31")

    assert task.title == "Write tests"
    assert task.due_date == date(2026, 9, 30)
    assert task.completed is False


@pytest.mark.parametrize(
        "bad_date",
        ["30-09-2026", "2026/09/30", "2026-09-31", "2026-09-30T12:00:00"]
        )
def test_task_rejects_invalid_due_date(bad_date):
    with pytest.raises(ValueError):
        Task("Write tests", due_date=bad_date)


@pytest.mark.parametrize("bad_bool", [1, 0])
def test_task_rejects_non_boolean_completion(bad_bool):
    with pytest.raises(TypeError):
        Task(completed=bad_bool)
