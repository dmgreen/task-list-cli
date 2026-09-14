from task import Task


def test_task_stores_title():
    task = Task("Write tests")

    assert task.title == "Write tests"


def test_task_string_includes_title():
    task = Task("Write tests")

    assert str(task) == "Task: Write tests"
