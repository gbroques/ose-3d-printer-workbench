import os


def get_icon_path(icon_filename):
    return os.path.join(os.path.dirname(__file__), icon_filename)
