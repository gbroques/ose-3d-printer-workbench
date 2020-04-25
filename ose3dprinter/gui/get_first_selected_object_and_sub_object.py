from ose3dprinter.app.exceptions import AttachmentError


def get_first_selected_object_and_sub_object(selection_objects):
    """Gets first selected object and sub-object.

    :param selection_objects: List of selection objects;
                              from Gui.Selection.getSelectionEx()
    :type selection_objects: List of Gui::SelectionObject
    :raises AttachmentError: If there's not a single selected object,
                             and not a single sub-object.
    :return: First selected object and first sub-object
    :rtype: Two-element tuple containing object and sub-object
    """
    num_selected = len(selection_objects)
    if num_selected != 1:
        raise AttachmentError(
            'Selected {} instead of 1 element'.format(num_selected))
    first_selection_object = selection_objects[0]
    num_sub_objects = len(first_selection_object.SubObjects)
    if num_sub_objects != 1:
        message_template = 'Selected object has {} sub objects instead of 1'
        raise AttachmentError(
            message_template.format(num_sub_objects))

    return first_selection_object.Object, first_selection_object.SubObjects[0]
