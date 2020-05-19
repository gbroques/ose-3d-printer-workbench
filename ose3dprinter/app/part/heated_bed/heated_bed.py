import Part
from ose3dprinter.app.shape import move_parts


class HeatedBed:

    @staticmethod
    def make(size, placement, origin_translation_offset):
        dimensions = (size, size, 50.8)  # 50.8 mm = 2 inches
        bed = Part.makeBox(*dimensions)

        parts = [bed]
        move_parts(parts,
                   placement,
                   origin_translation_offset,
                   dimensions)

        # TODO: Why does this need to be a compound to visually center heated bed?
        return Part.makeCompound(parts)
