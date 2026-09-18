from input_handler import InputHandler
import pytest
from unittest.mock import Mock


@pytest.fixture
def task_list():
    task_list = Mock()
    task = Mock()
    task_list.tasks = [task]
    task_list.get_task.return_value = task
    return task_list


@pytest.fixture
def input_handler(task_list):
    return InputHandler(task_list)


def test_handle_input_with_valid_input_can_quit(input_handler):
    with pytest.raises(SystemExit):
        input_handler.handle_input("Q")
    with pytest.raises(SystemExit):
        input_handler.handle_input("q")
    with pytest.raises(SystemExit):
        input_handler.handle_input("Quit")
    with pytest.raises(SystemExit):
        input_handler.handle_input("quit")


def test_handle_input_with_valid_input_invokes_create(input_handler,
                                                      monkeypatch):
    mock_create = Mock()
    monkeypatch.setattr("input_handler.InputHandler.create", mock_create)
    input_handler.handle_input("C")
    input_handler.handle_input("c")
    input_handler.handle_input("Create")
    input_handler.handle_input("create")
    assert mock_create.call_count == 4


def test_handle_input_with_valid_input_invokes_update(input_handler,
                                                      monkeypatch):
    mock_update = Mock()
    monkeypatch.setattr("input_handler.InputHandler.update", mock_update)
    input_handler.handle_input("U")
    input_handler.handle_input("u")
    input_handler.handle_input("Update")
    input_handler.handle_input("update")
    assert mock_update.call_count == 4


def test_update_on_invalid_task_number_catches_error(monkeypatch):
    task_list = Mock()
    task_list.get_task.side_effect = Mock(side_effect=IndexError)

    input_handler = InputHandler(task_list)
    monkeypatch.setattr("builtins.input", lambda _: "1")

    input_handler.update()

    task_list.get_task.assert_called_once_with(1)


@pytest.mark.parametrize(
        "answers, error_type",
        [
            (["1", "T", ""], ValueError),
            (["1", "D", "01-01-2026"], ValueError),
            (["1", "C", "True"], KeyError)
        ]
)
def test_update_with_invalid_input_catches_error(
    monkeypatch, answers, error_type
):
    task_list = Mock()
    task = Mock()
    task_list.tasks = [task]
    task_list.get_task.return_value = task
    task.update.side_effect = Mock(side_effect=error_type)

    input_handler = InputHandler(task_list)
    answers = iter(answers)
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    input_handler.update()

    task_list.get_task.assert_called_once_with(1)


def test_update_with_invalid_property_catches_error(monkeypatch):
    task_list = Mock()
    task = Mock()
    task_list.tasks = [task]
    task_list.get_task.return_value = task
    input_handler = InputHandler(task_list)
    answers = iter(["1", "Z"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    input_handler.update()

    task_list.get_task.assert_called_once_with(1)
    task.update.assert_not_called()


def test_update_can_change_title(monkeypatch):
    task_list = Mock()
    task = Mock()
    task_list.tasks = [task]
    task_list.get_task.return_value = task

    input_handler = InputHandler(task_list)
    answers = iter(["1", "T", "Updated task"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    input_handler.update()

    task_list.get_task.assert_called_once_with(1)
    task.update.assert_called_once_with(title="Updated task")


def test_update_can_change_due_date_to_new_date(monkeypatch):
    task_list = Mock()
    task = Mock()
    task_list.tasks = [task]
    task_list.get_task.return_value = task

    input_handler = InputHandler(task_list)
    answers = iter(["1", "D", "2026-09-30"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    input_handler.update()

    task_list.get_task.assert_called_once_with(1)
    task.update.assert_called_once_with(due_date="2026-09-30")


def test_update_can_clear_due_date(monkeypatch):
    task_list = Mock()
    task = Mock()
    task_list.tasks = [task]
    task_list.get_task.return_value = task

    input_handler = InputHandler(task_list)
    answers = iter(["1", "D", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    input_handler.update()

    task_list.get_task.assert_called_once_with(1)
    task.update.assert_called_once_with(due_date=None)


@pytest.mark.parametrize(
    "user_input, expected_call",
    [
        ("Y", True),
        ("y", True),
        ("N", False),
        ("n", False),
    ]
)
def test_update_can_change_completion(monkeypatch, user_input, expected_call):
    task_list = Mock()
    task = Mock()
    task_list.tasks = [task]
    task_list.get_task.return_value = task

    input_handler = InputHandler(task_list)
    answers = iter(["1", "C", user_input])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    input_handler.update()

    task_list.get_task.assert_called_once_with(1)
    task.update.assert_called_once_with(completed=expected_call)


def test_update_can_cancel(monkeypatch):
    task_list = Mock()
    task = Mock()
    task_list.tasks = [task]
    task_list.get_task.return_value = task

    input_handler = InputHandler(task_list)
    answers = iter(["1", "X"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    input_handler.update()

    task_list.get_task.assert_called_once_with(1)
    task.update.assert_not_called()


def test_input_handler_creates_and_adds_task(input_handler, monkeypatch):
    task_constructor = Mock()
    new_task = Mock()
    task_constructor.return_value = new_task
    monkeypatch.setattr("task.Task", task_constructor)

    input_handler.create()

    new_task.create_from_input.assert_called_once()
    input_handler.task_list.add_task.assert_called_once_with(new_task)
