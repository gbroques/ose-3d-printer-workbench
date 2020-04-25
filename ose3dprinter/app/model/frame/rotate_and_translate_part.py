def rotate_and_translate_part(part, d):
    """Rotate and translate a part.

    TODO: Come up with a better name than "d"
          to describe the combination of a rotation and translation.
          Maybe instead of a dictionary with "rotate_args" and "translation",
          we use FreeCAD.Placement objects to transfer this information.

    :param part: A part.
    :type part: FreeCAD.Part
    :param d: Dictionary containing 'rotate_args' and 'translation' keys.
    :type d: dict
    """
    rotate_args = d['rotate_args']
    is_list_of_lists = all(isinstance(e, list) for e in rotate_args)
    if is_list_of_lists:
        for args in rotate_args:
            part.rotate(*args)
    else:
        part.rotate(*rotate_args)
    part.translate(d['translation'])
