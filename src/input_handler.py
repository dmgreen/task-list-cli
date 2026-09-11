class InputHandler:
    options_str = (
        " [C]reate a new task",
        " [P]rint your tasks",
        " [U]pdate an existing task",
        " [D]elete a task",
        " [Q]uit"
    )

    def __init__(self, task_list):
        self.task_list = task_list

    def handle_input_loop(self):
        while True:
            print("Options: ")
            print("\n".join(self.options_str))
            choice = input(">>> ").strip().upper()
            if choice == 'C':
                self.create()
            elif choice == 'P':
                self.read()
            elif choice == 'U':
                self.update()
            elif choice == 'D':
                self.delete()
            elif choice == 'Q':
                print("Exiting the application.")
                break
            else:
                print("Invalid choice. Please try again.")

    def create(self):
        print("Selected create. Heading back to loop.")

    def read(self):
        print("Selected read. Heading back to loop.")

    def update(self):
        print("Selected update. Heading back to loop.")

    def delete(self):
        print("Selected delete. Heading back to loop.")
