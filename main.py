"""Command-line entry point for the task list application."""

from sys import argv

from task_list import TaskList
from input_handler import InputHandler


def main(args) -> None:
    """Run the task list CLI."""
    print("Task List CLI")
    if len(args) > 2:
        print("Error: Too many arguments provided.")
        exit(1)
    file_path = args[1] if len(args) == 2 else None
    tl = TaskList(file_path)
    print(f"Loaded {len(tl.tasks)} tasks from {tl.file_path}.")
    InputHandler(tl).handle_input_loop()


if __name__ == "__main__":
    main(argv)
