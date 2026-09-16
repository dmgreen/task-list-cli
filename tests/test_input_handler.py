from input_handler import InputHandler
from task_list import TaskList
import pytest
from unittest.mock import Mock


@pytest.fixture
def task_list(tmp_path):
    return TaskList(tmp_path / "tasks.json")


@pytest.fixture
def input_handler(task_list):
    return InputHandler(task_list)


def test_handle_input_with_valid_input_can_quit(input_handler, monkeypatch):
    with pytest.raises(SystemExit):
        input_handler.handle_input("Q")
    with pytest.raises(SystemExit):
        input_handler.handle_input("q")
    with pytest.raises(SystemExit):
        input_handler.handle_input("Quit")
    with pytest.raises(SystemExit):
        input_handler.handle_input("quit")


def test_handle_input_with_valid_input_can_create(input_handler, monkeypatch):
    mock_create = Mock()
    monkeypatch.setattr("input_handler.InputHandler.create", mock_create)
    input_handler.handle_input("C")
    input_handler.handle_input("c")
    input_handler.handle_input("Create")
    input_handler.handle_input("create")
    assert mock_create.call_count == 4


def test_handle_input_with_valid_input_can_read():
    pass


def test_handle_input_with_valid_input_can_update():
    pass


def test_handle_input_with_valid_input_can_delete():
    pass


def test_handle_input_with_invalid_input_shows_error():
    pass


def test_input_handler_creates_and_adds_task(input_handler, monkeypatch):
    class MockTask:
        def __init__(self):
            self.title = None

        def create_from_input(self):
            self.title = "Mock Task Title"

        def due_date(self):
            return None

    monkeypatch.setattr("task.Task", MockTask)
    input_handler.create()
    assert len(input_handler.task_list.tasks) == 1
    assert isinstance(input_handler.task_list.tasks[0], MockTask)
