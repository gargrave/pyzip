from app.commands.command_basic import BasicCommand
from app.config import config as config
from app.globals import gl as gl


class RemoveCommand(BasicCommand):

    def __init__(self):
        super().__init__()

    def start(self, final_callback):
        """
        Starts the process of removing a project.
        :param callback: (function) The callback method to invoke when the process is done.
        """
        super().start(final_callback)
        self.list_projects(self.input_loop)

    def input_loop(self):
        """
        Requests input from the user on which project to remove.
        """
        gl.console.log_line('Which project do you want to remove?')
        gl.console.log_line('Enter "l" to re-list the projects.', False)
        self.process_input(self.get_user_input())

    def begin_command(self, choice):
        """
        Begins the process of removing a project from the list.
        :param choice: (string) The value entered by the user.
        """
        try:
            project_to_remove = config.get_project_by_index(int(choice))
            gl.console.log_msg([
                'Remove the following project? [yN]',
                project_to_remove['name']])
            # if user confirms, remove it; anything else will return to input loop
            if self.get_user_input() == 'y':
                self.remove_project_from_list(int(choice))
            else:
                self.list_projects(self.input_loop)
        except ValueError:
            gl.console.log_err([
                'Invalid Project Index: {}'.format(choice),
                'Please enter the index from one of the projects listed.'
            ])
            self.list_projects(self.input_loop)

    def remove_project_from_list(self, idx):
        """
        Performs the action of removing the specified project from the list.
        :param choice: (int) The index of the project to remove.
        """
        config.remove_project(idx)
        self.resume_input_loop()
