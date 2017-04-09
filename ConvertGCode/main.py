import os
import parse

# define input and output file directory and names
file_directory = r'C:\Users\johno\Desktop\BBBS_painting'
draw_file_name = 'layer_4_formatted.nc'
paint_file_name = 'layer_4_paint.nc'

draw_file_path = os.path.join(file_directory, draw_file_name)
paint_file_path = os.path.join(file_directory, paint_file_name)

# convert gcode drawing to painting
parse.parse_gcode_draw_file(draw_file_path, paint_file_path)