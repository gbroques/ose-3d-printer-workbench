from .get_axis_frame_attachment_kwargs import AxisFrameAttachmentError


def get_first_selected_object_and_sub_object(selection):
    """Gets first selected object and sub-object.

    :param selection: Selection object from Gui.Selection.getSelectionEx()
    :type selection: Gui::SelectionObject
    :raises AxisFrameAttachmentError: If there's not a single selected object,
                                      and not a single sub-object.
    :return: First selected object, and first sub-object
    :rtype: Tuple of object and sub-object
    """
    num_selected = len(selection)
    if num_selected != 1:
        raise AxisFrameAttachmentError(
            'Selected {} instead of 1 element'.format(num_selected))
    first_selection = selection[0]
    num_sub_objects = len(first_selection.SubObjects)
    if num_sub_objects != 1:
        message_template = 'Selected object has {} sub objects instead of 1'
        raise AxisFrameAttachmentError(
            message_template.format(num_sub_objects))

    return first_selection.Object, first_selection.SubObjects[0]
