from app.utils.console import Console


class Globals:

    # dummy paths for testing
    TEST_CATEGORY = 'TEST_CATEGORY'
    TEST_NAME = 'TEST_PROJECT'
    TEST_PATH = '/TEST/PATH'
    TEST_COPYTO = '/TEST/COPYTO/PATH'

    def __init__(self):
        self.console = None

    def setup(self, title='Untitled'):
        # create a console/logger for the app
        self.console = Console(title)

gl = Globals()
