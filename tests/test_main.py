import json

from main import main


def test_main_saves_tasks_on_quit(tmp_path, monkeypatch):
    file_path = tmp_path / "tasks.json"
    answers = iter(["c", "Write tests", "2026-09-30", "q"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    assert main(["main.py", str(file_path)]) == 0

    output = json.loads(file_path.read_text())[0]

    assert output["id"] is not None
    assert output["title"] == "Write tests"
    assert output["due_date"] == "2026-09-30"
    assert output["completed"] is False


def test_main_returns_error_for_bad_task_file(tmp_path, monkeypatch, capsys):
    file_path = tmp_path / "tasks.json"
    file_path.write_text("not json")
    monkeypatch.setattr("builtins.input", lambda _: "q")

    assert main(["main.py", str(file_path)]) == 1
    assert "Error:" in capsys.readouterr().out
