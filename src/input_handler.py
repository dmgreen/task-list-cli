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

    def create(self):
        new_task = task.Task()
        try:
            new_task.create_from_input()
        except ValueError as e:
            print(f"Error creating task: {e}")
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
                title = input("Enter new title: ")
                task.update(title=title)
            elif property_choice == "D":
                due_date = input("Enter new due date (YYYY-MM-DD, optional): ")
                task.update(due_date=due_date or None)
            elif property_choice == "C":
                completed = input("Completed (y/n): ")
                completion_values = {
                    "Y": True,
                    "N": False,
                }
                try:
                    completed = completion_values[completed.strip().upper()]
                except KeyError as error:
                    raise ValueError(
                        "completion must be y or n"
                    ) from error
                task.update(completed=completed)
            else:
                raise ValueError("invalid property choice")
        except (IndexError, TypeError, ValueError) as error:
            print(f"Error updating task: {error}")
        else:
            self.task_list.sort()
            print("Task updated.")

    def delete(self):
        print("Selected delete. Heading back to loop.")

    def quit(self):
        print("Exiting the application.")
        exit(0)
