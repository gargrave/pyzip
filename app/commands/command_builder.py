import os

import app.utils.tools as tools


class CommandBuilder:

    def __init__(self):
        self._full_name = ''

    def get_full_command(self, input_path):
        """
        Returns the full command to call 7zip on this OS.
        :return: (string) the full command to call 7zip on this OS
        """
        # build the base file name, the full output path,
        # and return the full command required to call 7zip; quotes are
        # added around the two file paths to account for potential spaces
        base_name = '{}-{}'.format(os.path.basename(input_path), tools.get_date_string())
        self.full_name = os.path.join(os.path.dirname(input_path), base_name)
        return '{} {} "{}" "{}"'.format(self.app_path, self.args, self.full_name, input_path)

    @property
    def args(self):
        """
        Returns the args to pass to 7zip, based on the OS.
        :return: (string) the args to pass to 7zip, based on the OS.
        """
        return 'a -mx9' if tools.is_win() else 'a -mx9 -x!_MACOSX'

    @property
    def app_path(self):
        """
        Returns the full path to 7zip, based on the OS.
        :return: (string) the full path to 7zip, based on the OS
        """
        if tools.is_win():
            return 'C:\\Program Files\\7-Zip\\7z.exe'
        else:
            return '/Applications/Keka.app/Contents/Resources/keka7z'

    @property
    def full_name(self):
        """
        Returns the full path and name of the archive to be created.
        :return: (string) the full path and name of the archive to be created
        """
        return '{}.7z'.format(self._full_name)

    @full_name.setter
    def full_name(self, value):
        """
        Sets the value of this instance's _full_name field.
        """
        self._full_name = value
