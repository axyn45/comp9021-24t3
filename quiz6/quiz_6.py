# Written by *** for COMP9021
#
# Here are the stripes of width 1 of length 2 (minimal), 3 and 4:
#
# *
#   *
#
# *
#   *
#     *
#
# *
#   *
#     *
#       *
#
# Here are the stripes of width 2 of length 2 (minimal), 3 and 4:
#
#   *
# *   *
#   *
#
#   *
# *   *
#   *   *
#     *
#
#   *
# *   *
#   *   *
#     *   *
#       *
#
# Here are the stripes of width 3 of length 2 (minimal), 3 and 4:
#
#     *
#   *   *
# *   *
#   *
#
#     *
#   *   *
# *   *   *
#   *   *
#     *
#
#     *
#   *   *
# *   *   *
#   *   *   *
#     *   *
#       *
#
# For a given width, returns the maximal size (required to be
# at least equal to 2 * width) of stripes of that width,
# the number of such stripes, and a grid that captures them.
#
# Note that stripes can overlap.


from collections import defaultdict
from random import seed, random
import sys


dim = 10

def display(grid):
    print('  ', '-' * (2 * dim + 3))
    for row in grid:
        print('   |', *row, '|')
    print('  ', '-' * (2 * dim + 3))

def stripes(width):
    return 0, 0, grid
    # REPLACE THE RETURN STATEMENT ABOVE WITH YOUR CODE
    
# POSSIBLY DEFINE OTHER FUNCTIONS

try:
    for_seed, width, density = input('Input an integer, an integer '
                                     'greater than 0,\n      and '
                                     'a number between 0 and 1: '
                                    ).split()

    for_seed, width, density = int(for_seed), int(width), float(density)
    if width < 1 or density < 0 or density > 1:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
seed(for_seed)
grid = [['*' if random() < density else ' ' for _ in range(dim)]
             for _ in range(dim)
       ]
print('Here is the grid that has been generated:')
display(grid)

count, size, new_grid = stripes(width)
if not count:
    print(f'There are no stripes of width {width} in the grid!')
else:
    print(f'The size of the largest stripes of width is {size}.')
    print('There', count == 1 and 'is' or 'are', count,
          count == 1 and 'stripe' or 'stripes',
          'of that size.'
         )
    print('Here', count == 1 and 'it is:\n' or 'they are:')
    display(new_grid)
