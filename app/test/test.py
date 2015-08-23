import unittest

from app.commands.command_add import AddCommand
from app.config import config as config
from app.globals import gl as gl


class ConfigTest(unittest.TestCase):

    def setUp(self):
        config.load_config()

    def test_contains_project_by_name(self):
        # empty string should raise exception
        with self.assertRaises(ValueError):
            config.contains_project_by_name('')
        # should get True from our test project
        self.assertTrue(config.contains_project_by_name(gl.TEST_NAME))
        # should get False from a random string
        self.assertFalse(config.contains_project_by_name('j8f23hldfh9qw8ehf'))

    def test_contains_project_at_path(self):
        # empty string should raise exception
        with self.assertRaises(ValueError):
            config.contains_project_at_path('')
        # should get True from our test path
        self.assertTrue(config.contains_project_at_path(gl.TEST_PATH))
        # should get False from a random string
        self.assertFalse(config.contains_project_at_path('j8f23hldfh9qw8ehf'))

    def test_contains_category(self):
        # should get True from 'Uncategorized' - our default category
        self.assertTrue(config.contains_category(gl.TEST_CATEGORY))
        # should get False from a random string
        self.assertFalse(config.contains_category('j8f23hldfh9qw8ehf'))


class CmdAddTest(unittest.TestCase):

    def setUp(self):
        self.add = AddCommand()

    def test_check_project_path(self):
        # empty string should raise
        with self.assertRaises(ValueError):
            self.add.check_path('')
        # non-existant path should raise
        with self.assertRaises(ValueError):
            self.add.check_path('/Users/lskdjfals/jdkfjajj')
        # existing project with this path should raise
        with self.assertRaises(ValueError):
            self.add.check_path(gl.TEST_PATH)

if __name__ == '__main__':
    unittest.main()
