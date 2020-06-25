"""Package containing icons."""
import os


def get_icon_path(icon_filename: str) -> str:
    """Get the path to a given icon.

    :param icon_filename: icon filename (e.g. Box.svg)
    :type icon_filename: str
    :return: Path to icon file.
    :rtype: str
    """
    return os.path.join(os.path.dirname(__file__), icon_filename)


__all__ = ['get_icon_path']
