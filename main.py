"""Command-line entry point for the task list application."""

from sys import argv

from input_handler import InputHandler
from task_list import TaskFileError, TaskList


def main(args) -> int:
    """Run the task list CLI."""
    print("Task List CLI")
    if len(args) > 2:
        print("Error: Too many arguments provided.")
        exit(1)
    file_path = args[1] if len(args) == 2 else None
    try:
        tl = TaskList(file_path)
    except TaskFileError as error:
        print(f"Error: {error}")
        return 1
    print(f"Loaded {len(tl.tasks)} tasks from {tl.file_path}.")
    input_handler = InputHandler(tl)
    while True:
        print("\n".join(input_handler.options_str))
        if input_handler.handle_input(input(">>> ")):
            break
    try:
        tl.save()
    except TaskFileError as error:
        print(f"Error: {error}")
        return 1
    return 0


if __name__ == "__main__":
    main(argv)
