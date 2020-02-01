from FreeCAD import Console, Placement, Rotation, Vector


def get_placement_strategy(orientation):
    return {
        'x': (get_placement_for_left_face, get_placement_for_right_face),
        'y': (get_placement_for_front_face, get_placement_for_rear_face),
        'z': (get_placement_for_bottom_face, get_placement_for_top_face),
    }[orientation]


def get_placement_for_left_face(frame, face):
    x = face.Placement.Base.x
    y = frame.Shape.BoundBox.YMax
    z = frame.Shape.BoundBox.ZMax
    placement = Placement(
        Vector(x, y, z), Rotation(-90, 0, 90), Vector(0, 0, 0))
    translation_reference_point = Vector(0, 0, 1)
    return placement, translation_reference_point


def get_placement_for_right_face(frame, face):
    x = frame.Shape.BoundBox.XMax
    y = frame.Shape.BoundBox.YMax
    z = frame.Shape.BoundBox.ZMax
    placement = Placement(
        Vector(x, y, z), Rotation(-90, 0, -90), Vector(0, 0, 0))
    translation_reference_point = Vector(0, 0, 0)
    return placement, translation_reference_point



def get_placement_for_front_face(frame, face):
    x = face.CenterOfMass.x
    y = face.Placement.Base.y
    z = frame.Shape.BoundBox.ZMax
    placement = Placement(
        Vector(x, y, z), Rotation(0, 90, 90), Vector(0, 0, 0))
    translation_reference_point = Vector(0.5, 0, 0)
    return placement, translation_reference_point


def get_placement_for_rear_face(frame, face):
    x = face.CenterOfMass.x
    y = frame.Shape.BoundBox.YMax
    z = frame.Shape.BoundBox.ZMax
    placement = Placement(
        Vector(x, y, z), Rotation(0, 90, -90), Vector(0, 0, 0))
    translation_reference_point = Vector(-0.5, 0, 0)
    return placement, translation_reference_point


def get_placement_for_bottom_face(frame, face):
    Console.PrintMessage('Attaching axis to bottom face is not supported.\n')
    placement = Placement()
    translation_reference_point = Vector()
    return placement, translation_reference_point


def get_placement_for_top_face(frame, face):
    x = face.Placement.Base.x
    y = face.CenterOfMass.y
    z = frame.Shape.BoundBox.ZMax
    placement = Placement(
        Vector(x, y, z), frame.Placement.Rotation, Vector(0, 0, 0))
    translation_reference_point = Vector(0, 0.5, 0)
    return placement, translation_reference_point
