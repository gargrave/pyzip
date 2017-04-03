from app.globals import gl as gl
from app.config import config as config
from app.inputcommand import InputCommand
from app.commands.command_add import AddCommand
from app.commands.command_remove import RemoveCommand
from app.commands.command_zip import ZipCommand


class Pyzip:

    def __init__(self):
        """
        Ctor for the main class. initializes the app!
        """
        gl.setup('PyZip')
        gl.console.print_banner()

        # load config, and if everything goes okay, proceed
        if not config.load_config():
            self.commands = [
                InputCommand('a', self.do_add,
                             'Add a new project to the list'),
                InputCommand('l', self.do_list, 'List all available commands'),
                InputCommand('r', self.do_remove,
                             'Remove an existing project'),
                InputCommand('q', self.do_quit, 'Quit the application'),
                InputCommand('z', self.do_zip, 'Create an archive')
            ]
            self.input_loop()
        # otherwise, we will have to quit
        else:
            gl.console.log_err([
                'The app could not be properly initialized,',
                'and will have to exit now... :('
            ])

    def input_loop(self):
        """
        Requests input from the user for the next action.
        """
        gl.console.log_line('What do you want to do?')
        gl.console.log_line('(Enter "l" to list commands.)', False)

        # wait for user input
        raw_input = input('> ')
        cmd = raw_input.lower().strip()
        action = None

        # check the user's input against available commands
        for command in self.commands:
            if cmd == command.key:
                action = command.action
                break

        # if we found an action for the supplied comand, do it
        # otherwise, loop back to the top
        if action:
            action()
        else:
            print('Unknown command: "{}"'.format(cmd))
            self.input_loop()

    def return_to_input_loop(self):
        """
        Prints the app banner and returns to the main input loop.
        """
        gl.console.print_banner()
        self.input_loop()

    def do_add(self):
        """
        Starts the process of adding a new project to the list.
        """
        AddCommand().start(self.return_to_input_loop)

    def do_zip(self):
        """
        Starts the process of creating an archive.
        """
        ZipCommand().start(self.return_to_input_loop)

    def do_remove(self):
        """
        Starts the process of removing an existing project.
        """
        RemoveCommand().start(self.return_to_input_loop)

    def do_list(self):
        """
        Lists all available commands and a description of each.
        """
        command_list = ['{} : {}'.format(cmd.key, cmd.desc)
                        for cmd in self.commands]
        gl.console.log_msg(['Commands', ''] + command_list)
        self.input_loop()

    def do_quit(self):
        """
        Exits the application.
        """
        gl.console.log_msg(['Goodbye!', 'Thanks for using pyzip!'])
