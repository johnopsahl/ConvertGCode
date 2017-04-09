from math import cos, sin
import trig
import data
import fourthaxis


def convert_to_paint(paint_gcode_file, plunge_state):

    # sets local variables equal to global variables;
    x_move_end = data.x_end
    y_move_end = data.y_end

    # calculate the total draw distance for the move
    draw_dist_total = ((x_move_end - data.x_start)**2 + (y_move_end - data.y_start)**2)**0.5

    # angle between vector and horizontal
    theta = trig.atan3(y_move_end - data.y_start, x_move_end - data.x_start)

    # if tool does not have infinite axial symmetry, then evaluate what angle the brush should be rotated to
    if data.tool_axial_symmetry != 2:
        data.a_end = fourthaxis.calc_fourth_axis_angle(theta, data.a_start, data.a_offset, data.tool_axial_symmetry)
        data.a_start = data.a_end

    draw_dist = draw_dist_total

    # indicates which paint move code is on during processing of a single gcode line
    paint_move_count = 0

    # loop until line of gcode is complete
    while draw_dist > 0:

        if data.clean_brush_dist <= 0: # when paint brush drys out, wet and dry brush, dip in paint
            clean_brush(2, 2, paint_gcode_file)
            dip_brush(2, paint_gcode_file)
            data.paint_dist = data.paint_dist_max
            data.clean_brush_dist = data.max_clean_brush_dist

        if data.paint_dist == 0:  # when paint brush runs out of paint, dip in paint
            dip_brush(1, paint_gcode_file)
            data.paint_dist = data.paint_dist_max

        # if it is the first move of the gcode command line and the tool doesn't have infinite axial symmetry
        if paint_move_count == 0 and data.tool_axial_symmetry != 2:
            paint_gcode_file.write('G0 A%.15f\n' % data.a_end)

        #  ****************************************************
        #  define custom a axis movements here
        # if paint_move_count == 0:
        #     if data.a_end == 0:
        #         data.a_end = 60
        #     elif data.a_end == 60:
        #         data.a_end = 120
        #     elif data.a_end == 120:
        #         data.a_end = 60
        #
        #     paint_gcode_file.write('G0 A%.15f\n' % data.a_end)
        #  ***************************************************

        if data.paint_dist == data.paint_dist_max:
            paint_gcode_file.write('G0 Z%.15f\n' % data.z_plunge)
        elif plunge_state is True:
            paint_gcode_file.write('G0 Z%.15f\n' % data.z_plunge)
            plunge_state = False

        if data.paint_dist > draw_dist:
            # paint the entire draw distance
            data.clean_brush_dist -= draw_dist
            data.paint_dist -= draw_dist
            draw_dist = 0

            paint_gcode_file.write('G1 X%.15f Y%.15f F%i\n' % (x_move_end, y_move_end, data.feed_rate))

            # set start points of next move as end points of this move
            data.x_start = x_move_end
            data.y_start = y_move_end

        elif data.paint_dist == draw_dist:
            # paint the entire draw distance
            data.clean_brush_dist -= data.paint_dist
            data.paint_dist = 0
            draw_dist = 0

            paint_gcode_file.write('G1 X%.15f Y%.15f F%i\n' % (x_move_end, y_move_end, data.feed_rate))

            # set start points of next move as end points of this move
            data.x_start = x_move_end
            data.y_start = y_move_end

        elif data.paint_dist < draw_dist:
            # paint for the paint distance on the draw distance
            draw_dist -= data.paint_dist
            data.clean_brush_dist -= data.paint_dist

            # calculate segment end points at draw_dist along movement

            # determine the x and y coordinates when the brush will run out of paint
            data.x_end = data.paint_dist*cos(theta) + data.x_start
            data.y_end = data.paint_dist*sin(theta) + data.y_start

            # write the g code command to the paint file
            paint_gcode_file.write('G1 X%.15f Y%.15f F%i\n' % (data.x_end, data.y_end, data.feed_rate))

            # all paint on brush has been used
            data.paint_dist = 0

            # set start points of next move as end points of this move
            data.x_start = data.x_end
            data.y_start = data.y_end

        paint_move_count += 1


def clean_brush(water_dip_count, towel_wipe_count, paint_gcode_file):
    # clean brush during painting to re-wet brush or between colors

    # dip brush in water in a ccw circle
    paint_gcode_file.write('G0 Z%.15f\n' % data.z_retract)
    paint_gcode_file.write('G0 X%.15f Y%.15f\n' % (data.x_water + data.water_dip_radius / 2, data.y_water))
    paint_gcode_file.write('G0 Z%.15f\n' % data.z_water_dip)

    for i in range(0, water_dip_count):
        paint_gcode_file.write('G3 X%.15f Y%.15f I%.15f J%.15f F%i\n'
                               % (data.x_water - data.water_dip_radius / 2, data.y_water, -data.water_dip_radius / 2, 0,
                                  data.feed_rate))
        paint_gcode_file.write('G3 X%.15f Y%.15f I%.15f J%.15f F%i\n'
                               % (data.x_water + data.water_dip_radius / 2, data.y_water, data.water_dip_radius / 2, 0,
                                  data.feed_rate))

    # wipe brush on towel in a ccw motion
    paint_gcode_file.write('G0 Z%.15f\n' % data.z_retract)
    paint_gcode_file.write('G0 X%.15f Y%.15f\n' % (data.x_towel + data.towel_wipe_radius / 2, data.y_towel))
    paint_gcode_file.write('G0 Z%.15f\n' % data.z_towel_wipe)

    for j in range(0, towel_wipe_count):
        paint_gcode_file.write('G3 X%.15f Y%.15f I%.15f J%.15f F%i\n'
                               % (data.x_towel - data.towel_wipe_radius / 2, data.y_towel, -data.towel_wipe_radius / 2, 0,
                                  data.feed_rate))
        paint_gcode_file.write('G3 X%.15f Y%.15f I%.15f J%.15f F%i\n'
                               % (data.x_towel + data.towel_wipe_radius / 2, data.y_towel, data.towel_wipe_radius / 2, 0,
                                  data.feed_rate))

    # increment center of towel to prevent
    data.y_towel += 2.5


def dip_brush(paint_dip_count, paint_gcode_file):

    from random import uniform
    from math import pi

    random_radius = uniform(0, data.paint_dip_radius)
    random_angle = uniform(0, 2*pi)

    x_paint = random_radius*cos(random_angle) + data.x_paint
    y_paint = random_radius*sin(random_angle) + data.y_paint

    # dip brush in paint
    paint_gcode_file.write('G0 Z%.15f\n' % data.z_retract)
    paint_gcode_file.write('G0 X%.15f Y%.15f\n' % (x_paint, y_paint))

    for i in range(0, paint_dip_count):
        paint_gcode_file.write('G0 Z%.15f\n' % data.z_paint_dip)
        paint_gcode_file.write('G0 Z%.15f\n' % data.z_retract)

    paint_gcode_file.write('G0 X%.15f Y%.15f\n' % (data.x_start, data.y_start))