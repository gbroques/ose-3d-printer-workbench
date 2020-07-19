import Part
from FreeCAD import Placement, Vector
from osecore.app.shape import move_parts


class HeatedBed:
    """Heated bed to help prevent warping of prints.

    See Also:
        * https://wiki.opensourceecology.org/wiki/Heated_Bed
        * https://reprap.org/wiki/Heated_Bed
    """

    @staticmethod
    def make(size: float = 203.2,  # 8 inches
             initial_placement: Placement = Placement(),
             origin_translation_offset: Vector = Vector()) -> Part.Compound:
        """Make heated bed.

        :param size: [description]
        :param initial_placement: Initial placement for part.
        :param origin_translation_offset: Offset part from origin.
        :return: Heated bed object.
        """
        dimensions = (size, size, 50.8)  # 50.8 mm = 2 inches
        bed = Part.makeBox(*dimensions)

        parts = [bed]
        move_parts(parts,
                   initial_placement,
                   origin_translation_offset,
                   dimensions)

        # TODO: Why does this need to be a compound to visually center heated bed?
        return Part.makeCompound(parts)
