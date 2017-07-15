import argparse
import random
import turtle

seed = random.getrandbits(64)
print('Randomness Seed = {}'.format(seed))
random.seed(seed)
# favorites: 7052490615248054880
#            2082863135281490600

# Fractal Paramaters
complexity   = 10
angle        = 32.72
length       = 200
length_ratio = 0.65
angle_ratio  = 0.5
bg_color     = 'black'
modify_width = True
modify_color = True


#
# gen_color_range()
# Desc: Generates a range (list) of RGB color values (each value being a
#       6-digit color value) that gradually transitions from color1 to color2.
#       The length of the list depends on the biggest difference between the
#       Red, Green, or Blue values of color1 and color2.
# Args: color1 - a 6-digit hex string.
#       color2 - a 6-digit hex string.
# Returns: a list of 6-digit hex strings.
#
def gen_color_range(color1, color2):
    r1 = int(color1[0:2], 16)
    g1 = int(color1[2:4], 16)
    b1 = int(color1[4:6], 16)
    r2 = int(color2[0:2], 16)
    g2 = int(color2[2:4], 16)
    b2 = int(color2[4:6], 16)

    r_diff = r2 - r1
    g_diff = g2 - g1
    b_diff = b2 - b1

    max_diff = max(abs(r_diff), abs(g_diff), abs(b_diff))

    r_step = float(r_diff) / max_diff
    g_step = float(g_diff) / max_diff
    b_step = float(b_diff) / max_diff

    color_range = []
    for step in range(max_diff):
        r = r1 + int(step * r_step)
        g = g1 + int(step * g_step)
        b = b1 + int(step * b_step)

        color_range.append('{:02X}{:02X}{:02X}'.format(r, g, b))

    return color_range


# Generate a range of color values from one random color to another
color_range = []
num_colors = 2
color_old = '{:06X}'.format(random.getrandbits(24))
for i in range(num_colors):
    color_new = '{:06X}'.format(random.getrandbits(24))
    color_range += gen_color_range(color_old, color_new)
    color_old = color_new
div = len(color_range) / complexity


#
# canopy()
#
def canopy(n, angle, length):
    if n == 0:
        return
    else:
        if modify_width:
            turtle.width(max(0, n-2))
        if modify_color:
            turtle.pencolor('#{}'.format(color_range[n*div-1]))

        #######################################################################
        # Left
        random_angle_ratio = random.uniform(angle_ratio*0.6, angle_ratio*1.4)
        turtle.left(angle*random_angle_ratio)
        turtle.forward(length)

        # Recursion #
        canopy(
            n=n-1,
            angle=random.randint(int(angle*0.75), int(angle*1.5)),
            length=length*random.uniform(length_ratio*0.6, length_ratio*1.4)
        )

        if modify_width:
            turtle.width(max(0, n-2))
        if modify_color:
            turtle.pencolor('#{}'.format(color_range[n*div-1]))

        #######################################################################
        # Right
        turtle.backward(length)
        turtle.right(angle)
        turtle.forward(length)

        # Recursion #
        canopy(
            n=n-1,
            angle=random.randint(int(angle*0.75), int(angle*1.5)),
            length=length*random.uniform(length_ratio*0.6, length_ratio*1.4)
        )

        if modify_width:
            turtle.width(max(0, n-2))
        if modify_color:
            turtle.pencolor('#{}'.format(color_range[n*div-1]))

        turtle.backward(length)
        turtle.left(angle*(1-random_angle_ratio))

#
# main()
#
def main():
    if modify_width:
        turtle.width(complexity-1)
    if modify_color:
        turtle.pencolor('#{}'.format(color_range[complexity*div-1]))

    # Set the background color of the canvas
    turtle.bgcolor(bg_color)

    # Start the turtle facing the correct direction, with enough space to draw
    # the fractal visibly.
    turtle.left(90)
    turtle.pu()
    turtle.backward(length)
    turtle.pd()
    turtle.forward(length)

    canopy(complexity, angle, length*length_ratio)

    turtle.exitonclick()


if __name__ == '__main__':

    # Used if run from a terminal, e.g.:
    #   python tactal.py
    parser = argparse.ArgumentParser()

    # Complexity
    parser.add_argument('--complexity', '-c', type=int, default=complexity, nargs=1,
                        help='The degree of complexity, i.e., the number of '
                             'iterations of the fractal.')
    # Angle
    parser.add_argument('--angle', '-a', type=float, default=angle, nargs=1,
                        help='The angle between two branches.')
    # Length
    parser.add_argument('--length', '-l', type=int, default=length, nargs=1,
                        help='The starting length of the branch.')
    # Length Ratio
    parser.add_argument('--length_ratio', '-r', type=float, default=length_ratio, nargs=1,
                        help='The ratio of lengths between parent and child '
                             'branches.')
    # Angle Ratio
    parser.add_argument('--angle_ratio', '-g', type=float, default=angle_ratio, nargs=1,
                        help='The ratio of angle between two sibling branches.')
    # Background Color
    parser.add_argument('--bg_color', '-b', default=bg_color, nargs=1,
                        help='The background color to set the canvas to. A '
                             'string, either a standard color (e.g. "orange") '
                             'or hex value (e.g. "#800080").')
    # Modify Width
    parser.add_argument('--modify_width', action='store_true',
                        help='Modify the width of the line: longer branches '
                             'are thicker, shorter branches are thinner.')
    # Modify Color
    parser.add_argument('--modify_color', action='store_true',
                        help='Modify the width of the line: longer branches '
                             'are thicker, shorter branches are thinner.')

    args = parser.parse_args()

    complexity   = args.complexity
    angle        = args.angle
    length       = args.length
    length_ratio = args.length_ratio
    angle_ratio  = args.angle_ratio
    bg_color     = args.bg_color
    modify_width = args.modify_width
    modify_color = args.modify_color

    main()
