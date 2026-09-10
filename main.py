"""Command-line entry point for the task list application."""

from sys import argv

from task_list import task_list

def main(args) -> None:
	"""Run the task list CLI."""
	print("Task List CLI")
	if len(args) > 2:
		print("Error: Too many arguments provided.")
		exit(1)
	file_path = args[1] if len(args) == 2 else None
	tl = task_list(file_path)
	print(f"Loaded {len(tl.tasks)} tasks from {tl.file_path}.") 


if __name__ == "__main__":
	main(argv)
