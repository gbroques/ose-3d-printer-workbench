import os


def get_resource_path(resource_name):
    return os.path.join(os.path.dirname(__file__), resource_name)
