import json
import os

from app.globals import gl as gl


# the name of the file for reading/writing config
CONFIG_FILE = os.path.join(os.path.expanduser('~'),
                           'Documents/PyzipConfig.json')


class Config:

    def __init__(self):
        self.config = None
        self.indexed_projects = None
        # the highest index possible for selecting a project
        self._max_index = 0

    def load_config(self):
        # load config data from disk
        try:
            with open(CONFIG_FILE, 'r') as json_file:
                self.config = json.load(json_file)
        # for file-not-found errors, just create one
        except FileNotFoundError:
            return self.__create_new_config()
        # for other IO errors, print the message and return
        except OSError as e:
            gl.console.log_err([
                'There was an issue creating the new file:',
                str(e)
            ])
            return True

    def __create_new_config(self):
        """
        Creates an empty app config and writes a new file to disk
        :return: True if there are any errors; otherwise False.
        """
        gl.console.log_msg([
            'No "{}" config file was found on disk.'.format(CONFIG_FILE),
            'A new one will be created now...'
        ])
        # create an empty config object
        self.config = {
            'projects': [
                {
                    'category': gl.TEST_CATEGORY,
                    'list': [
                        {
                            'path': gl.TEST_PATH,
                            'name': gl.TEST_NAME,
                            'copyTo': gl.TEST_COPYTO
                        }
                    ]
                }
            ]
        }
        # write it out to a new JSON file
        try:
            with open(CONFIG_FILE, 'w') as new_json_file:
                json.dump(self.config, new_json_file, indent=4)
        # for any errors, print the message and return True
        except OSError as e:
            gl.console.log_err([
                'There was an issue creating the new file:',
                str(e)
            ])
            return True

    def __can_test_projects(self, input_string):
        """
        Ensures that our projects list has been loaded, and that
        the property being tested is not empty.
        :param input_string: (string) The string to test
        """
        # make sure the config file has been loaded
        if not self.config:
            return 'config.load_config() has not been called'
        # make sure we didn't get an empty string
        if not input_string:
            return 'param "{}" cannot be empty.'

    def get_indexed_project_list(self):
        """
        Returns a list of projects and their indices. Use this for
            displaying a list of all of the projects with the numbers
            needed to work on them.
        :return: (List) A list of projects and their respective indices.
        """
        # create a new list to print to the console, with indices
        print_list = []
        index = 0
        self.indexed_projects = []
        # the full list of projects
        projects = self.config['projects']

        # begin by looping through each category, which is an array of projects
        for project_set in projects:
            category_name = project_set['category']
            project_list = project_set['list']

            # skip the test category
            if category_name == gl.TEST_CATEGORY:
                continue
            # skip empty categories
            if len(project_list) == 0:
                continue

            # add the category's name onto the list for printing
            print_list.append('** {} **'.format(category_name))
            print_list.append('')

            # loop through each project in this category
            for project in project_list:
                # make sure the path to the project is valid, and add it to the
                # list
                if os.path.exists(project['path']):
                    self.indexed_projects.append(project)
                    print_list.append(
                        '  [{}] - {}'.format(index, project['name']))
                    index += 1
            print_list.append('')

        # use the new list to get the highest index
        self.max_index = len(self.indexed_projects) - 1
        return print_list

    def get_project_by_index(self, idx):
        """
        Returns a project from the local list at the given index.
        :param idx: (int) The index of the project to fetch.
        :return: (dict) The project at the requested index.
        """
        if idx < 0 or idx > self.max_index:
            raise ValueError
        return self.indexed_projects[idx]

    def add_new_project(self, project_specs):
        """
        Creates a new project and stores it in the local config file.
        :param project_specs: (ProjectSpecs) The project settings to be stored
        """
        new_project = {
            'name': project_specs.name,
            'path': project_specs.path
        }
        #  save the 'copy_to' path, if one has been specified
        if project_specs.copy_to:
            new_project['copyTo'] = project_specs.copy_to

        # add the new project to our local config dict
        new_category = project_specs.category
        # if the category exists in the current list, add this project there
        found = False
        for p in self.config['projects']:
            if p['category'] == new_category:
                found = True
                p['list'].append(new_project)
        # otherwise, create a new category set
        if not found:
            self.config['projects'].append({
                'category': new_category,
                'list': [new_project]
            })

        # then write the whole thing to disk
        # we are simply dumping the full contents to the file here,
        # so no need to worry about opening for appending
        try:
            with open(CONFIG_FILE, 'w') as json_file:
                json.dump(self.config, json_file, indent=4)
        except OSError as e:
            gl.console.log_err([
                'There was an error writing the config data to disk:',
                str(e)])

    def remove_project(self, idx):
        """
        Removes a project from the current list, and updates the file on disk.
        :param idx: (int) The index of the project to remove.
        """
        gl.console.log_todo('Remove project: {}'.format(
            self.indexed_projects[idx]['name']))

    def contains_project_by_name(self, name):
        """
        Scans the existing projects to see if one with the specified
        name is already defined.
        :param name: The name to search for.
        :return: True if the name is already in use; otherwise False.
        """
        # make sure the config file has been loaded
        # and we did not get an empty string
        err = self.__can_test_projects(name)
        if err:
            raise ValueError(err.format('name'))

        # TODO oppotunity for refactoring with this loop (and the one below)
        # scan the current projects for the specified name
        for project_set in self.config['projects']:
            for proj in project_set['list']:
                if proj['name'] == name:
                    return True
        return False

    def contains_project_at_path(self, path):
        """
        Scans the existing projects to see if one with the specified
        path is already defined.
        :param path: (string) The path to search for.
        :return: True if the path is already in use; otherwise False.
        """
        # make sure the config file has been loaded
        # and we did not get an empty string
        err = self.__can_test_projects(path)
        if err:
            raise ValueError(err.format('path'))

        # scan the current projects for the specified path
        for project_set in self.config['projects']:
            for proj in project_set['list']:
                if proj['path'] == path:
                    return True
        return False

    def contains_category(self, category):
        """
        Returns whether the specified category is in our project list.
        :return: True if the category is in use; otherwise False.
        """
        for project_set in self.config['projects']:
            if project_set['category'] == category:
                return True
        return False

    @property
    def max_index(self):
        return self._max_index

    @max_index.setter
    def max_index(self, value):
        self._max_index = value

config = Config()
