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

    assert str(task_list) == "1. Task: First task\n2. Task: Second task"
