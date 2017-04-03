import os

import app.utils.tools as tools
from app.commands.command_basic import BasicCommand
from app.config import config as config
from app.globals import gl as gl
from app.projectspecs import ProjectSpecs


class AddCommand(BasicCommand):

    def __init__(self):
        super().__init__()
        self.new_project = ProjectSpecs()

    def start(self, final_callback):
        super().start(final_callback)
        self.get_project_name()

    def get_project_name(self):
        """
        Prompts the user to enter a name for the new project.
        """
        print('\nWhat do you want to name the new project?')
        project_name = input('> ').strip()

        # if we get an empty string, loop back
        if not project_name:
            gl.console.log_err('Project name cannot be empty!')
            self.get_project_name()
        # check for the 'quit' command
        elif project_name.lower() == 'q':
            super().end_command()
        # ensure that this name is not already in use
        elif config.contains_project_by_name(project_name):
            gl.console.log_err('There is already a project with that name!')
            self.get_project_name()
        # otherwise, confirm the name of the project, and
        # either continue to the next step or loop back
        else:
            print('Use the name "{}" for this project? [Yn]'.format(
                project_name))
            choice = input('> ').lower().strip()
            if choice == 'n':
                self.get_project_name()
            else:
                self.new_project.name = project_name
                self.get_project_path()

    def get_project_path(self):
        """
        Prompts the user to enter the path the new project.
        """
        print('\nWhat is the full path of the project?')
        project_path = input('> ').strip()

        # check for the 'quit' command
        if project_path.lower() == 'q':
            return super().end_command()
        try:
            # test the input for any path errors
            self.check_path(project_path)
        except ValueError as e:
            # for any errors, display the error and loop back to the top
            gl.console.log_err(str(e))
            return self.get_project_path()

        # confirm with the user that it is correct
        if self.confirm_path(project_path):
            if tools.is_win():
                print(project_path)
            self.new_project.path = project_path.replace('\\', '/')
            self.check_for_category()
        else:
            self.get_project_path()

    def check_for_copyto_path(self):
        """
        Prompts the user to see if a "copyTo" path should be
        added to the new project.
        """
        print('\nWould you like to add a "copyTo" path? [Yn]')
        choice = input('> ').lower().strip()

        # check for the 'quit' command
        if choice == 'q':
            return super().end_command()
        elif choice == 'n':
            return self.save_new_project()
        else:
            self.get_copyto_path()

    def get_copyto_path(self):
        """
        Prompts the user for the path of the 'copyTo' property.
        """
        print('\nWhere would you like the archive copied to?')
        copyto_path = input('> ').strip()

        # check for the 'quit' command
        if copyto_path.lower() == 'q':
            return super().end_command()
        try:
            # test the input for any path errors
            self.check_path(copyto_path, False)
        except ValueError as e:
            # for any errors, display the error and loop back to the top
            gl.console.log_err(str(e))
            return self.get_copyto_path()

        # confirm with the user that it is correct
        if self.confirm_path(copyto_path):
            self.new_project.copy_to = copyto_path.replace('\\', '/')
            self.save_new_project()
        else:
            self.get_copyto_path()

    def check_for_category(self):
        """
        Checks with the user if the project should have a category.
        """
        print('\nWhat category would you like to use?')
        print('(Default is \'Uncategorized\')')
        category = input('> ').strip()

        # check for the 'quit' command
        if category.lower() == 'q':
            return super().end_command()
        else:
            print('\nUse this category? [Yn]')
            print('\'{}\''.format(category))

            choice = input('> ').strip()
            if choice == 'n':
                return self.check_for_category()
            else:
                self.new_project.category = category
                self.check_for_copyto_path()

    def check_path(self, path, ensure_unique=True):
        """
        Confirms that the specified path is a valid value.
        """
        # check for emptry string
        if not path:
            raise ValueError('Project path cannot be empty!')
        # confirm that the path exists
        elif not os.path.exists(path):
            raise ValueError(
                'The specified path does not exist on this system.')
        # confirm that path is not already in use
        elif ensure_unique and config.contains_project_at_path(path):
            raise ValueError(
                'That path is already in use. Please try another.')

    def confirm_path(self, path):
        """
        Prints the path back to the user for confirmation.
        :param path: (string) The path the user has entered.
        """
        print('\nUse the following path? [Yn]')
        print(path)
        choice = input('> ').lower().strip()
        return choice != 'n'

    def save_new_project(self):
        """
        Sends the new data to the config manager to update the file.
        """
        config.add_new_project(self.new_project)
        self.check_for_next_add()

    def check_for_next_add(self):
        """
        Checks with the user to see if another project needs to be added.
        """
        print('\nAll done! Would you like to add another project? [yN]')
        choice = input('> ').lower().strip()

        if choice == 'y':
            # start the process again
            self.get_project_name()
        else:
            # return to the main menu
            self.end_command()
