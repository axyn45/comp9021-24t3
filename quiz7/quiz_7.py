# Written by *** for COMP9021
#
# Working with a grid of size 10 x 10, with i and j
# interpreted as follows:
#
#              j
#     1 2 3 4 5 6 7 8 9 10
#   1
#   2
#   3
#   4
# i 5
#   6
#   7
#   8
#   9
#  10
#
# Finds the longest path in the grid starting from (i, j),
# moving up diagonally in the NE direction (↗)
# or moving down diagonally in the SW direction (↙),
# moving SE to change direction.
#
# Moving up to start with.
#
# To make the path unique, we prefer moving in a given direction
# (up or down) for as long as possible.


from random import seed, random
import sys

dim = 10

def display(grid):
    print('  ', '-' * (2 * dim + 3))
    for row in grid:
        print('   |', *row, '|')
    print('  ', '-' * (2 * dim + 3))

def longest_path(i, j, grid):
    return 0, [[' ' * dim] for _ in range(dim)]
    # REPLACE THE RETURN STATEMENT ABOVE WITH YOUR CODE

# POSSIBLY DEFINE OTHER FUNCTIONS
    
try:
    for_seed, i, j, density = input('Input an integer, two integers between '
                                    f'1 and {dim},\n      '
                                    'and a number between 0 and 1: '
                                   ).split()

    for_seed, i, j, density = int(for_seed), int(i), int(j), float(density)
    if i < 1 or i > dim or j < 1 or j > dim or density < 0 or density > 1:
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

path_length, path_in_grid = longest_path(i, j, grid)
if not path_length:
    print(f'There is no special path starting from ({i}, {j}) in the grid!')
else:
    print(f'The longest special path starting from ({i}, {j}) '
          f'has a length of {path_length}.'
          )
    print('Here it is:')
    display(path_in_grid)
