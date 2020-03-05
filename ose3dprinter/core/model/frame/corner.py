class Corner:
    BOTTOM_LEFT_FRONT = 'bottom_left_front'
    BOTTOM_LEFT_REAR = 'bottom_left_rear'
    BOTTOM_RIGHT_REAR = 'bottom_right_rear'
    BOTTOM_RIGHT_FRONT = 'bottom_right_front'
    TOP_LEFT_FRONT = 'top_left_front'
    TOP_LEFT_REAR = 'top_left_rear'
    TOP_RIGHT_REAR = 'top_right_rear'
    TOP_RIGHT_FRONT = 'top_right_front'


def is_top_corner(corner):
    return (
        corner == Corner.TOP_LEFT_FRONT or
        corner == Corner.TOP_LEFT_REAR or
        corner == Corner.TOP_RIGHT_REAR or
        corner == Corner.TOP_RIGHT_FRONT
    )
