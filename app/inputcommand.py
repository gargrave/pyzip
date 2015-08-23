class InputCommand:

    def __init__(self, key, action, desc):
        # the input key to call this command
        self.key = key
        # the function to call when this command is called
        self.action = action
        # the description of this command
        self.desc = desc
