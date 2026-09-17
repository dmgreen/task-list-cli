import pytest
from task import Task
from task_list import TaskList


def test_empty_task_list_has_no_tasks_message(tmp_path):
    task_list = TaskList(tmp_path / "tasks.json")

    assert task_list.tasks == []
    assert str(task_list) == "No tasks available."


def test_task_list_renders_tasks_in_order(tmp_path):
    task_list = TaskList(tmp_path / "tasks.json")
    task_list.add_task(Task("First task"))
    task_list.add_task(Task("Second task"))

    assert str(task_list) == (
        "1. First task (Due: None, Completed: False)\n"
        "2. Second task (Due: None, Completed: False)"
    )


def test_get_tasks_accepts_valid_task_number(tmp_path):
    task_list = TaskList(tmp_path / "tasks.json")
    task_list.add_task(Task("First task"))

    task = task_list.get_task(1)

    assert task.title == "First task"


@pytest.mark.parametrize("task_number", [0, 2])
def test_get_task_rejects_invalid_task_number(tmp_path, task_number):
    task_list = TaskList(tmp_path / "tasks.json")
    task_list.add_task(Task("First task"))

    with pytest.raises(IndexError):
        task_list.get_task(task_number)


def test_task_list_sorts_tasks(tmp_path):
    task_list = TaskList(tmp_path / "tasks.json")
    first_task = Task("First task", "2026-09-20")
    second_task = Task("Second task", "2026-09-30")
    task_list.add_task(first_task)
    task_list.add_task(second_task)

    first_task.update(due_date="2026-10-10")
    task_list.sort()

    assert [task.title for task in task_list.tasks] == [
        "Second task",
        "First task",
    ]
