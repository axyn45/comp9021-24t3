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
    global grid
    result={}
    maxlen=0
    # countmax=0
    def checkDiagno(i,j):
        length=0
        for idx1 in range(len(grid[i])-j):
            for idx2 in range(width):
                if(i+idx1+idx2>=len(grid) or not grid[i+idx1+idx2][j+idx1-idx2]=='*'):
                    if(length>1):
                        result[(i,j)]=length
                        # maxlen=length if length>maxlen else maxlen
                    return length
            length+=1
        result[(i,j)]=length
        return length

    
    def isRepeated(i,j):
        for k,v in result.items():
            if(j-i==k[1]-k[0]):
                return True
        return False
    
    def maxStrips(maxlen):
        # global grid
        countmax=0
        gridmax=[[' ' for _ in range(dim)] for _ in range(dim)]
        # gridmax=[]
        for k,v in result.items():
            if(v==maxlen):
                countmax+=1
                for i in range(k[0],k[0]+width+v-1):
                    for j in range(k[1]-width+1,k[1]+v):
                        if((k[0]+k[1])%2==(i+j)%2 and k[0]-k[1]+2*width-2>=i-j>=k[0]-k[1] and k[0]+k[1]+2*v-2>=i+j>=k[0]+k[1]):
                            gridmax[i][j]='*'
        return gridmax,countmax
                

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if(not grid[i][j]=='*' or j<width-1 or i>=len(grid[i])-1 or i+width>len(grid)-1):
                continue
            if(not isRepeated(i,j)):
                length=checkDiagno(i,j)
                if(length>maxlen):maxlen=length
    # print(result)



    gridmax,countmax=maxStrips(maxlen)
    return countmax, maxlen*width, gridmax
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
