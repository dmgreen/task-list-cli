import task


class InputHandler:
    options_str = (
        " [C]reate a new task",
        " [P]rint your tasks",
        " [U]pdate an existing task",
        " [D]elete a task",
        " [Q]uit"
    )
    cmd_dict = {
        "C": "create",
        "P": "read",
        "U": "update",
        "D": "delete",
        "Q": "quit"
    }

    def __init__(self, task_list):
        self.task_list = task_list

    def handle_input(self, cmd):
        cmd = cmd.strip().upper()
        if len(cmd) == 0 or cmd[0] not in self.cmd_dict:
            print("Invalid choice. Please try again.")
            return

        getattr(self, self.cmd_dict[cmd[0]])()

    @staticmethod
    def _prompt_title(prompt):
        title = input(prompt).strip()
        if not title:
            raise ValueError("Task title is required")
        return title

    @staticmethod
    def _prompt_due_date(prompt):
        return input(prompt).strip() or None

    @staticmethod
    def _prompt_completion(prompt):
        completion_values = {
            "Y": True,
            "N": False,
        }
        try:
            return completion_values[input(prompt).strip().upper()]
        except KeyError as error:
            raise ValueError("completion must be y or n") from error

    def create(self):
        try:
            title = self._prompt_title("Enter task title: ")
            due_date = self._prompt_due_date(
                "Enter due date (YYYY-MM-DD, optional): "
            )
            new_task = task.Task(title=title, due_date=due_date)
        except (TypeError, ValueError) as error:
            print(f"Error creating task: {error}")
            return
        self.task_list.add_task(new_task)

    def read(self):
        # TODO: remove this as a user option. Display tasks after each action.
        print("Current tasks:")
        print(self.task_list)

    def update(self):
        if not self.task_list.tasks:
            print("No tasks available to update.")
            return

        print("Current tasks:")
        print(self.task_list)

        try:
            task_number = int(input("Enter task number to update: ").strip())
            task = self.task_list.get_task(task_number)

            property_choice = input(
                "Update [T]itle, [D]ue date, [C]ompleted, or [X]ancel: "
            ).strip().upper()

            if property_choice == "X":
                return

            if property_choice == "T":
                task.update(title=self._prompt_title("Enter new title: "))
            elif property_choice == "D":
                due_date = self._prompt_due_date(
                    "Enter new due date (YYYY-MM-DD, optional): "
                )
                task.update(due_date=due_date)
            elif property_choice == "C":
                completed = self._prompt_completion("Completed (y/n): ")
                task.update(completed=completed)
            else:
                raise ValueError("invalid property choice")
        except (IndexError, TypeError, ValueError) as error:
            print(f"Error updating task: {error}")
        else:
            self.task_list.sort()
            print("Task updated.")

    def delete(self):
        if not self.task_list.tasks:
            print("No tasks available to delete.")
            return

        print("Current tasks:")
        print(self.task_list)

        try:
            task_number = int(input("Enter task number to delete: ").strip())
            selected_task = self.task_list.get_task(task_number)
            confirmation = input(
                f'Delete "{selected_task.title}"? [Y]es/[N]o/[X]ancel: '
            ).strip().upper()

            if confirmation in ("N", "X"):
                return
            if confirmation != "Y":
                raise ValueError("invalid confirmation choice")

            self.task_list.delete_task(task_number)
        except (IndexError, TypeError, ValueError) as error:
            print(f"Error deleting task: {error}")
        else:
            print("Task deleted.")

    def quit(self):
        print("Exiting the application.")
        exit(0)
