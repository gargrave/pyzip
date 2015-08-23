import os


class Console:

    def __init__(self, title='Untitled'):
        # the length of the lines to display in the banner
        self.line_len = 57
        # the char to use for building the border lines
        self.line_char = '-'
        # the full line to print in banner borders
        self.border_line = self.build_line()
        # the title line of the border
        self.title_line = self.build_title_line(title)
        # the string to put around special logging types
        self.log_str = '*'
        self.clear_line = '\x1b[2J\x1b[H'

    def print_banner(self, clear=True):
        """
        Prints the full title banner to the console.
        :param clear: (Boolean) Whether the console should be cleared
            before the banner is printed (default is True).
        """
        if clear:
            self.clear()
        print(self.border_line)
        print(self.title_line)
        print(self.border_line)

    def build_line(self):
        """
        Builds the line to use for the banner's borders.
        :return: (string) the line to use for the banner's borders.
        """
        new_line = self.line_char
        while new_line.__len__() < self.line_len:
            new_line += self.line_char
        return new_line

    def build_title_line(self, title):
        """
        Builds the title line for the banner.
        :param title: (string) The title to use for the banner.
        :return: (string) The new title for the banner.
        """
        # desired length = title, padding with one * and one space on each side
        target_len = self.line_len - 4
        # truncate titles that are too long
        if title.__len__() > target_len:
            title = title[:target_len]
        # for even calcuations, make sure the title has
        # an odd number of digits
        if title.__len__() % 2 == 0:
            title += ' '
        new_line = title
        # pad with spaces until it is the desired lenth
        while new_line.__len__() < target_len:
            new_line = ' {} '.format(new_line)
        return '{} {} {}'.format(
            self.line_char, new_line, self.line_char)

    def log_line(self, msg, empty_line_on_top=True):
        """
        Prints one or more lines to the console with no decorations.
        :param msg: (string or list of strings) The line or lines to
            print to the console.
        :param empty_line_on_top: (Boolean) Whether a blank line should be
            printed ahead of the other lines (default is True).
        """
        if empty_line_on_top:
            print()
        if type(msg) == str:
            msg = [msg]
        for m in msg:
            print(m)

    def log_msg(self, msg):
        """
        Logs a bordered message to the console.
        :param msg: (string or list of strings) The message (or messages) to log.
        """
        if type(msg) == str:
            msg = [msg]
        print()
        print(self.border_line)
        for m in msg:
            print('- {}'.format(m))
        print(self.border_line)

    def log_todo(self, msg):
        """
        Logs a message with 'TODO' added to the top of it.
        :param msg: (string or list of strings) The message (or messages) to log.
        """
        if type(msg) == str:
            msg = [msg]
        self.log_msg(['{s} TODO {s}'.format(s=self.log_str)] + msg)

    def log_err(self, msg):
        """
        Logs a message with 'ERROR' added to the top of it.
        :param msg: (string or list of strings) The message (or messages) to log.
        """
        if type(msg) == str:
            msg = [msg]
        self.log_msg(['{s} ERROR {s}'.format(s=self.log_str), ''] + msg)

    def clear(self):
        """
        Clears the current console window.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
