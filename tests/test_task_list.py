import json
from datetime import date

import pytest

from task import Task
from task_list import TaskFileError, TaskList


def test_default_task_file_uses_user_data_directory(tmp_path, monkeypatch):
    monkeypatch.setattr("task_list.user_data_dir", lambda _: str(tmp_path))

    task_list = TaskList()

    assert task_list.file_path == tmp_path / "tasks.json"


def test_default_task_file_is_not_created_in_current_directory(
    tmp_path, monkeypatch
):
    user_data_path = tmp_path / "user-data"
    working_directory = tmp_path / "working-directory"
    working_directory.mkdir()
    monkeypatch.setattr(
        "task_list.user_data_dir", lambda _: str(user_data_path)
    )
    monkeypatch.chdir(working_directory)

    task_list = TaskList()
    task_list.add_task(Task("First task"))
    task_list.save()

    assert (user_data_path / "tasks.json").exists()
    assert not (working_directory / "tasks.json").exists()


def test_explicit_task_file_overrides_default(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "task_list.user_data_dir", lambda _: str(tmp_path / "user-data")
    )
    explicit_path = tmp_path / "custom" / "tasks.json"

    task_list = TaskList(explicit_path)

    assert task_list.file_path == explicit_path


def test_empty_task_list_has_no_tasks_message(tmp_path):
    task_list = TaskList(tmp_path / "tasks.json")

    assert task_list.tasks == []
    assert task_list.to_str() == "No tasks available."


def test_task_list_renders_tasks_in_order(tmp_path):
    task_list = TaskList(tmp_path / "tasks.json")
    task_list.add_task(Task("First task"))
    task_list.add_task(Task("Second task"))

    assert task_list.to_str() == (
        "1. First task (Due: None, Completed: False)\n"
        "2. Second task (Due: None, Completed: False)"
    )


def test_task_list_renders_tasks_matching_filter(tmp_path):
    task_list = TaskList(tmp_path / "tasks.json")
    task_list.add_task(Task("Due task", "2026-09-22"))
    task_list.add_task(Task("Later task", "2026-09-30"))

    assert task_list.to_str(
        lambda task: task.due_date == date(2026, 9, 22)
    ) == "1. Due task (Due: 2026-09-22, Completed: False)"


def test_task_list_string_conversion_uses_default_rendering(tmp_path):
    task_list = TaskList(tmp_path / "tasks.json")
    task_list.add_task(Task("First task"))

    assert str(task_list) == task_list.to_str()


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


def test_delete_task_removes_selected_task(tmp_path):
    task_list = TaskList(tmp_path / "tasks.json")
    task_list.add_task(Task("First task"))
    task_list.add_task(Task("Second task"))

    task_list.delete_task(1)

    assert [task.title for task in task_list.tasks] == ["Second task"]


@pytest.mark.parametrize("task_number", [0, 2])
def test_delete_task_rejects_invalid_task_number(tmp_path, task_number):
    task_list = TaskList(tmp_path / "tasks.json")
    task_list.add_task(Task("First task"))

    with pytest.raises(IndexError):
        task_list.delete_task(task_number)


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


def test_task_list_round_trips_tasks_as_json(tmp_path):
    file_path = tmp_path / "tasks.json"
    task_list = TaskList(file_path)
    task_list.add_task(Task("Due task", "2026-09-30", True))
    task_list.add_task(Task("Open task"))

    task_list.save()
    loaded_task_list = TaskList(file_path)

    assert [(task.title, task.due_date, task.completed)
            for task in loaded_task_list.tasks] == [
        ("Due task", Task("Due task", "2026-09-30").due_date, True),
        ("Open task", None, False),
    ]
    assert json.loads(file_path.read_text()) == [
        {
            "id": task_list.tasks[0].id,
            "title": "Due task",
            "due_date": "2026-09-30",
            "completed": True,
        },
        {
            "id": task_list.tasks[1].id,
            "title": "Open task",
            "due_date": None,
            "completed": False,
        },
    ]


@pytest.mark.parametrize(
    "contents",
    [
        "not json",
        "{}",
        "[{}]",
        '[{"title": "Task", "due_date": "bad", "completed": false}]',
    ],
)
def test_task_list_rejects_bad_task_file(tmp_path, contents):
    file_path = tmp_path / "tasks.json"
    file_path.write_text(contents)

    with pytest.raises(TaskFileError):
        TaskList(file_path)


def test_task_list_missing_file_starts_empty(tmp_path):
    file_path = tmp_path / "new" / "tasks.json"
    task_list = TaskList(file_path)

    assert task_list.tasks == []


def test_save_does_not_create_missing_file_for_empty_task_list(tmp_path):
    file_path = tmp_path / "new" / "tasks.json"
    task_list = TaskList(file_path)

    task_list.save()

    assert not file_path.exists()


def test_save_creates_missing_file_when_tasks_exist(tmp_path):
    file_path = tmp_path / "new" / "tasks.json"
    task_list = TaskList(file_path)
    task_list.add_task(Task("First task"))

    task_list.save()

    assert json.loads(file_path.read_text()) == [
        {
            "id": task_list.tasks[0].id,
            "title": "First task",
            "due_date": None,
            "completed": False,
        },
    ]


def test_legacy_records_receive_ids_and_save_them(tmp_path):
    file_path = tmp_path / "tasks.json"
    file_path.write_text(
        '[{"title":"Old task","due_date":null,"completed":false}]'
    )

    task_list = TaskList(file_path)
    task_id = task_list.tasks[0].id

    assert task_id
    assert "id" not in json.loads(file_path.read_text())[0]
    task_list.save()
    assert json.loads(file_path.read_text())[0]["id"] == task_id


def test_task_list_can_find_and_delete_tasks_by_id(tmp_path):
    task_list = TaskList(tmp_path / "tasks.json")
    task = Task("Find me")
    task_list.add_task(task)

    assert task_list.get_task_by_id(task.id) is task
    task_list.delete_task_by_id(task.id)

    with pytest.raises(KeyError):
        task_list.get_task_by_id(task.id)


def test_save_preserves_existing_empty_task_file(tmp_path):
    file_path = tmp_path / "tasks.json"
    file_path.write_text("[]")
    task_list = TaskList(file_path)

    task_list.save()

    assert json.loads(file_path.read_text()) == []
