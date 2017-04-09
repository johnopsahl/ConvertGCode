import data
import brushpaint


def parse_gcode_draw_file(draw_file_path, paint_file_path):

    previous_command_number = -1
    command_number = -1
    line_count = 0
    line_count_total = file_length(draw_file_path)

    draw_gcode_file = open(draw_file_path, 'r')
    paint_gcode_file = open(paint_file_path, 'w')

    # for each line in the g code file
    for line in draw_gcode_file:
        line_count += 1
        line = line.strip()

        # g code command
        if line.startswith('G'):
            command_number = get_number(line, 'G')

            # rapid move
            if command_number == 0:

                if previous_command_number == 1:
                    paint_gcode_file.write('G0 Z%.15f\n' % data.z_retract)

                data.x_start = get_number(line, 'X')
                data.y_start = get_number(line, 'Y')
                paint_gcode_file.write(line + '\n')

            # linear move
            elif command_number == 1:

                    # TODO: create better logic than line_count != 2 to identify first G1 command
                    if previous_command_number == 0 and line_count != 2:
                        plunge_state = True
                    else:
                        plunge_state = False

                    data.x_end = get_number(line, 'X')
                    data.y_end = get_number(line, 'Y')
                    brushpaint.convert_to_paint(paint_gcode_file, plunge_state)

                    # retract after the last movement
                    if line_count == line_count_total:
                        paint_gcode_file.write('G0 Z%.15f\n' % data.z_retract)

            else:
                paint_gcode_file.write(line + '\n')

        else:
            paint_gcode_file.write(line + '\n')

        previous_command_number = command_number

    draw_gcode_file.close()
    paint_gcode_file.close()


def get_number(line, command_letter):

    # character immediately after command letter
    n = line.find(command_letter) + 1
    m = line.find(' ', n)

    # if no space is found in the current line
    if m == -1:
        return float(line[n:])
    else:
        return float(line[n:m])


def file_length(file_path):

    # count how many lines are in a file
    f = open(file_path, 'r')
    line_count_total = sum(1 for line in f)
    f.close()

    return line_count_total
