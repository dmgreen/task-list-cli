from datetime import date, timedelta
from unittest.mock import Mock

import pytest

from input_handler import InputHandler


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
    assert input_handler.handle_input("Q") is True
    assert input_handler.handle_input("q") is True
    assert input_handler.handle_input("Quit") is True
    assert input_handler.handle_input("quit") is True


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


def test_handle_input_with_valid_input_invokes_delete(input_handler,
                                                      monkeypatch):
    mock_delete = Mock()
    monkeypatch.setattr("input_handler.InputHandler.delete", mock_delete)
    input_handler.handle_input("D")
    input_handler.handle_input("d")
    input_handler.handle_input("Delete")
    input_handler.handle_input("delete")
    assert mock_delete.call_count == 4


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


def test_delete_can_delete_selected_task(monkeypatch):
    task_list = Mock()
    task = Mock(title="First task")
    task_list.tasks = [task]
    task_list.get_task.return_value = task

    input_handler = InputHandler(task_list)
    answers = iter(["1", "Y"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    input_handler.delete()

    task_list.get_task.assert_called_once_with(1)
    task_list.delete_task.assert_called_once_with(1)


@pytest.mark.parametrize("confirmation", ["N", "n", "X", "x"])
def test_delete_can_cancel(monkeypatch, confirmation):
    task_list = Mock()
    task = Mock(title="First task")
    task_list.tasks = [task]
    task_list.get_task.return_value = task

    input_handler = InputHandler(task_list)
    answers = iter(["1", confirmation])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    input_handler.delete()

    task_list.get_task.assert_called_once_with(1)
    task_list.delete_task.assert_not_called()


def test_delete_with_no_tasks_does_not_prompt(monkeypatch):
    task_list = Mock()
    task_list.tasks = []
    input_handler = InputHandler(task_list)
    prompt = Mock(side_effect=AssertionError("input should not be called"))
    monkeypatch.setattr("builtins.input", prompt)

    input_handler.delete()

    prompt.assert_not_called()
    task_list.delete_task.assert_not_called()


@pytest.mark.parametrize("task_number", ["0", "2", "not a number"])
def test_delete_with_invalid_task_number_does_not_delete(
    monkeypatch, task_number
):
    task_list = Mock()
    task = Mock(title="First task")
    task_list.tasks = [task]
    task_list.get_task.side_effect = IndexError
    input_handler = InputHandler(task_list)
    monkeypatch.setattr("builtins.input", lambda _: task_number)

    input_handler.delete()

    if task_number.isdigit():
        task_list.get_task.assert_called_once_with(int(task_number))
    else:
        task_list.get_task.assert_not_called()
    task_list.delete_task.assert_not_called()


def test_delete_with_invalid_confirmation_does_not_delete(monkeypatch):
    task_list = Mock()
    task = Mock(title="First task")
    task_list.tasks = [task]
    task_list.get_task.return_value = task
    input_handler = InputHandler(task_list)
    answers = iter(["1", "maybe"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    input_handler.delete()

    task_list.delete_task.assert_not_called()


def test_input_handler_creates_and_adds_task(input_handler, monkeypatch):
    task_constructor = Mock()
    new_task = Mock()
    task_constructor.return_value = new_task
    monkeypatch.setattr("task.Task", task_constructor)
    answers = iter(["Write tests", "2026-09-30"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    input_handler.create()

    task_constructor.assert_called_once_with(
        title="Write tests", due_date="2026-09-30"
    )
    input_handler.task_list.add_task.assert_called_once_with(new_task)


@pytest.mark.parametrize(
    "answers",
    [
        ["", "2026-09-30"],
        ["Write tests", "30-09-2026"],
    ]
)
def test_input_handler_does_not_add_task_for_invalid_creation_input(
    input_handler, monkeypatch, answers
):
    monkeypatch.setattr("builtins.input", lambda _: answers.pop(0))

    input_handler.create()

    input_handler.task_list.add_task.assert_not_called()


def test_read_prints_all_tasks(input_handler, monkeypatch, capsys):
    input_handler.task_list.to_str.return_value = "1. First task"
    monkeypatch.setattr("builtins.input", lambda _: "a")

    input_handler.read()

    assert capsys.readouterr().out == (
        "Current tasks:\n1. First task\n"
    )
    input_handler.task_list.to_str.assert_called_once_with()


def test_read_prints_tasks_due_today(input_handler, monkeypatch, capsys):
    input_handler.task_list.to_str.return_value = "1. Due task"
    monkeypatch.setattr("builtins.input", lambda _: "d")

    input_handler.read()

    assert capsys.readouterr().out == (
        f"Tasks due {date.today().isoformat()}:\n1. Due task\n"
    )
    filter_func = input_handler.task_list.to_str.call_args.args[0]
    assert filter_func(Mock(due_date=date.today())) is True
    tomorrow = date.today() + timedelta(days=1)
    assert filter_func(Mock(due_date=tomorrow)) is False


@pytest.mark.parametrize("view_choice", ["", "x"])
def test_read_rejects_invalid_view(input_handler, monkeypatch, capsys,
                                   view_choice):
    monkeypatch.setattr("builtins.input", lambda _: view_choice)

    input_handler.read()

    assert "Error printing tasks:" in capsys.readouterr().out
    input_handler.task_list.to_str.assert_not_called()
