import os
import shutil
import subprocess

import app.utils.tools as tools
from app.commands.command_basic import BasicCommand
from app.commands.command_builder import CommandBuilder
from app.config import config as config
from app.globals import gl as gl


class ZipCommand(BasicCommand):

    def __init__(self):
        super().__init__()
        self.cmd_builder = CommandBuilder()

    def start(self, final_callback):
        super().start(final_callback)
        self.list_projects(self.input_loop)

    def input_loop(self):
        """
        Requests input from the user on which project to zip.
        """
        gl.console.log_line('Which project do you want to zip?')
        gl.console.log_line('Enter "l" to re-list the projects.', False)
        self.process_input(self.get_user_input())

    def begin_command(self, choice):
        """
        Attempts to begin the zipping command. If any errors are encountered,
            we will return to the input loop for more user input.
        :param choice: (string) The value entered by the user.
        """
        try:
            self.run_zip_command(config.get_project_by_index(int(choice)))
        # for invalid values, print the error and start the loop over
        except ValueError:
            gl.console.log_err([
                'Invalid Project Index: {}'.format(choice),
                'Please enter the index from one of the projects listed.'
            ])
            self.input_loop()

    def run_zip_command(self, project):
        """
        Runs the 7zip command and builds the archive.
        """
        # get the full command for running 7zip
        cmd = self.cmd_builder.get_full_command(project['path'])
        # call the process to start creating the archive
        if tools.is_win():
            subprocess.call(cmd)
        elif tools.is_mac():
            subprocess.call(cmd, shell=True)

        # print the success message and return to the input loop
        gl.console.log_msg(
            ['Success!', 'The archive was successfully created.'])
        # check if there is a 'copyTo' property specified
        try:
            # the src/dest to copy the new archive to/from
            src = self.cmd_builder.full_name
            dest = project['copyTo']
            if os.path.exists(src) and os.path.exists(dest):
                gl.console.log_msg([
                    'The archive will now be copied to:',
                    dest,
                    'Please be patient...'
                ])
                shutil.copy2(src, dest)
                gl.console.log_msg(['The archive was successfully copied!'])
            else:
                gl.console.log_err([
                    'The project has a "copyTo" specified,',
                    'but the operation could not be completed.'
                ])
        except KeyError:
            # an error here simply means there is no 'copyTo',
            # so we can safely ignore it
            pass
        self.resume_input_loop()
