from math import pi


def calc_fourth_axis_angle(theta, angle_current, angle_offset, tool_axial_symmetry):
    # calculate absolute brush angle to be perpendicular to G01 movement

    # angle between vector and horizontal plus brush angle offset
    norm_angle_end = theta*180/pi + angle_offset

    # normalize the start angle to a value between 0 and 360 degrees
    norm_angle_current = angle_current % 360

    # no symmetry angle change
    angle_change = calc_angle_change(norm_angle_current, norm_angle_end)

    # if tool has 180 degree axial symmetry
    if tool_axial_symmetry == 1:

        # calculate angle change if tool has 180 deg axial symmetry
        angle_change_180 = calc_angle_change((norm_angle_current + 180) % 360, norm_angle_end)

        # if 180 deg angle change is less then use it
        if abs(angle_change_180) < abs(angle_change):
            angle_change = angle_change_180

    # add angle change to current angle for angle change
    angle_next = angle_current + angle_change

    # round to nearest degree; floating point errors occur otherwise
    angle_next = round(angle_next)

    return angle_next


def calc_angle_change(angle_start, angle_end):
    # determine which angle to rotate the brush to; normalized 0-360 deg range

    if angle_start > angle_end:
        if angle_start - angle_end < 180:  # small angle; clockwise
            angle_change = -(angle_start - angle_end)
        else:  # large angle; counter clockwise
            angle_change = 360 - (angle_start - angle_end)
    elif angle_start < angle_end:
        if angle_end - angle_start < 180:  # small angle: counter clockwise
            angle_change = angle_end - angle_start
        else:  # large angle; clockwise
            angle_change = -(360 - (angle_end - angle_start))
    else:  # same angle
        angle_change = 0

    return angle_change
