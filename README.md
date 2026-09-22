# Task List CLI

A small interactive command-line task list application written in Python. Tasks are stored in a JSON file so they persist between runs.

## Features

- Create tasks with an optional due date
- List existing tasks
- Update a task's title, due date, or completion status
- Delete tasks with confirmation
- Sort tasks by due date and then title
- Use a per-user default task file or provide a custom file path

## Requirements

- Python 3.9 or newer

The application uses `platformdirs` to choose a per-user data directory for its default task file.

## Usage

Run the application with the default task file. It is stored in the operating system's per-user application-data directory, so running the command from a workspace does not create a `tasks.json` file there:

```text
python main.py
```

The default location is typically `%APPDATA%\task-list-cli\tasks.json` on Windows, `~/Library/Application Support/task-list-cli/tasks.json` on macOS, and `~/.local/share/task-list-cli/tasks.json` on Linux.

Use a different JSON file by passing its path:

```text
python main.py path/to/my-tasks.json
```

The application displays an interactive menu:

| Command | Action |
| --- | --- |
| `C` | Create a new task |
| `P` | Print tasks |
| `U` | Update an existing task |
| `D` | Delete a task |
| `Q` | Save and quit |

Commands are case-insensitive. Due dates must use `YYYY-MM-DD` format. Leave a due-date prompt empty to omit or clear a due date.

## Data Format

Tasks are stored as a JSON array. Each task contains a title, an optional ISO-formatted due date, and a completion flag:

```json
[
  {
    "title": "Write documentation",
    "due_date": "2026-09-30",
    "completed": false
  }
]
```

If the selected file does not exist, the application starts with an empty task list and creates the file when tasks are saved.

## Development

Install the project in editable mode with its development tools:

```text
python -m pip install -e ".[dev]"
```

Run the test suite:

```text
pytest
```

Run the linter:

```text
ruff check .
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
