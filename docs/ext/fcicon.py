import os
import re

from docutils import nodes


def fcicon_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """FreeCAD Icon.

    Returns 2 part tuple containing list of nodes to insert into the
    document and a list of system messages.  Both are allowed to be
    empty.

    :param name: The role name used in the document.
    :param rawtext: The entire markup snippet, with role.
    :param text: The text marked with the role.
    :param lineno: The line number where rawtext appears in the input.
    :param inliner: The inliner instance that called us.
    :param options: Directive options for customization.
    :param content: The directive content for customization.
    """
    try:
        pattern = re.compile('([\w\s]+) \((sm|md|lg)\) \<(.*\.\w+)\>')
        result = pattern.search(text)
        if not result or len(result.groups()) != 3:
            raise ValueError
        alt, size, filename = result.groups()
    except ValueError:
        msg = inliner.reporter.error(
            'FreeCAD Icon must include alt, size (sm, md, or lg), and filename (e.g. :fcicon:`My Icon Alt (md) <MyIcon.svg>`); '
            '"%s" is invalid.' % text, line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]
    app = inliner.document.settings.env.app
    try:
        freecad_icon_directory = app.config.freecad_icon_directory
        if not freecad_icon_directory:
            raise AttributeError
    except AttributeError:
        raise ValueError(
            'freecad_icon_directory configuration value is not set')
    image = make_image_node(freecad_icon_directory, alt, size, filename)
    return [image], []


def make_image_node(freecad_icon_directory, alt, size, filename):
    """Create a link to a BitBucket resource.

    :param freecad_icon_directory: Directory to FreeCAD Icons.
    :param alt: Alt text of icon.
    :param size: Must be one of "sm" (small), "md", (medium), or "lg" (large).
    :param filename: Filename of icon.
    """
    dim = {
        'sm': '16px',  # small size, as it appears in the tree view.
        'md': '32px',  # medium size, regular buttons such as toolbars.
        'lg': '64'  # original size, large buttons.
    }[size]
    uri = os.path.join(freecad_icon_directory, filename)
    # Preface uri with forward slash to make path relative to root of docs.
    # TODO: Should '/' be os.path.sep for Windows?
    return nodes.image(uri='/' + uri, alt=alt, width=dim, height=dim)


def setup(app):
    """Install the plugin.

    :param app: Sphinx application context.
    """
    app.add_role('fcicon', fcicon_role)
    app.add_config_value('freecad_icon_directory', None, 'env')
