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
        new_task.create_from_input()
        self.task_list.add_task(new_task)

    def read(self):
        print("Current tasks:")
        print(self.task_list)

    def update(self):
        print("Selected update. Heading back to loop.")

    def delete(self):
        print("Selected delete. Heading back to loop.")

    def quit(self):
        print("Exiting the application.")
        exit(0)
