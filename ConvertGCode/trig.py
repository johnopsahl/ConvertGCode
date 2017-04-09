from math import atan2, pi


def atan3(dy, dx):
    # tangent function that recognizes positive and negative angles

    # rounding error causes some small negative numbers that should be zero
    # then tan3 function interprets as close to 2*pi instead of close to zero
    # set all small negative dy values equal to zero
    if -1e-15 < dy < 0.0:
        dy = 0.0

    angle = atan2(dy, dx)
    if angle < 0:
        angle += 2 * pi

    return angle
