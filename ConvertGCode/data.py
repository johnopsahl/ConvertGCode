# if not stated otherwise, units are mm

# initialize variables to zero
x_start = 0
y_start = 0
x_end = 0
y_end = 0
a_start = 0  # deg
a_end = 0  # deg
paint_dist = 0
clean_brush_dist = 0

# feed rate
feed_rate = 2500  # mm/min

# fourth axis
tool_axial_symmetry = 2  # 0 -> no axial symmetry, 1 -> 180 deg axial symmetry, 2 -> infinite axial symmetry
a_offset = 0 # deg

# max distance to paint before returning for more paint
paint_dist_max = 300

# clean brush after painting specified distance on the canvas
# needed because brush tends to dry out after a period of time
max_clean_brush_dist = 5000

# brush z positions
z_retract = 15
z_plunge = 0

# paint dip
x_paint = -12.5 - 22.5
y_paint = 107.5 - 42.5 - 42.5
z_paint_dip = 1.5
paint_dip_radius = 7.5

# water dip
x_water = -12.5 - 22.5 - 42.5
y_water = 107.5
z_water_dip = 1
water_dip_radius = 10

# towel wipe
x_towel = -12.5 - 22.5 - 21.25
y_towel = 190
z_towel_wipe = 0
towel_wipe_radius = 25
