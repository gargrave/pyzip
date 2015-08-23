class ProjectSpecs:

    def __init__(self):
        # the name of the project
        self.name = None
        # the path to the project on disk
        self.path = None
        # the category for the new project
        self.category = None
        # the (optional) "copyTo" property
        # this will specify a path to which the newly created
        # archive will be copied after the process is finished
        self.copy_to = None
