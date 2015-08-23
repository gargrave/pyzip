from app.globals import gl as gl
from app.config import config as config


class BasicCommand:

    def __init__(self):
        # the callback to call when this class is exiting
        self.final_callback = self.__quit

    def start(self, final_callback):
        """
        Begins the process of creating an archive from the list
        :param callback: the callback from calling class to be
            called when all processes have finished
        """
        self.final_callback = final_callback
        gl.console.clear()

    def input_loop(self):
        """
        Requests input from the user on which action to perform. This
            is a default implementation, and will most likely need to
            be overridden by the sub-class.
        """
        gl.console.log_line('Which do you want to do?')
        self.process_input(self.get_user_input())

    def resume_input_loop(self):
        """
        Checks if the user wants to return to the input loop for this
            command, or head back to the main menu.
        """
        gl.console.log_line('Do you want to do this to another project? [yN]')
        # anything but a 'y' will return us to the top menu
        if self.get_user_input() == 'y':
            self.list_projects(self.input_loop)
        else:
            self.end_command()

    def process_input(self, choice):
        """
        Process the input from the user.
            If 'l', re-print the projects list
            If 'q', exit immediately
            Otherwise, attempt to parse the input and zip that project
        :param choice: (string) The value entered by the user.
        """
        if choice == 'l':
            self.list_projects(self.input_loop)
        elif choice == 'q':
            self.end_command()
        else:
            self.begin_command(choice)

    def get_user_input(self):
        """
        Displays the caret prompt to request input from the user.
        :return: (string) The value inputted by the user.
        """
        return input('> ').lower().strip()

    def list_projects(self, callback=None):
        """
        Displays a list of the projects on this local machine, and the
        index required to call that project.
        """
        gl.console.log_msg(['Current Projects', ''] + config.get_indexed_project_list())
        if callback:
            callback()

    def begin_command(self, choice):
        """
        This is simply a place-holder method for beginning the command
            held by the sub-class. It will need to be full implemented
            by the sub-class.
        :param choice: (string) The value entered by the user.
        """
        pass

    def end_command(self):
        """ Ends the processes and returns to the previous process. """
        self.__quit()
        self.final_callback()

    # this is simply a default 'end' function
    def __quit(self):
        pass
