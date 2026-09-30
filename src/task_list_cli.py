"""Installed command-line entry point for the task list application."""

from sys import argv
from typing import Optional, Sequence

from input_handler import InputHandler
from task_list import TaskFileError, TaskList


def main(args: Optional[Sequence[str]] = None) -> int:
    """Run the task list CLI."""
    args = argv if args is None else args
    print("Task List CLI")
    if len(args) > 2:
        print("Error: Too many arguments provided.")
        exit(1)
    file_path = args[1] if len(args) == 2 else None
    try:
        task_list = TaskList(file_path)
    except TaskFileError as error:
        print(f"Error: {error}")
        return 1
    print(f"Loaded {len(task_list.tasks)} tasks from {task_list.file_path}.")
    input_handler = InputHandler(task_list)
    while True:
        print("\n".join(input_handler.options_str))
        if input_handler.handle_input(input(">>> ")):
            break
    try:
        task_list.save()
    except TaskFileError as error:
        print(f"Error: {error}")
        return 1
    return 0
