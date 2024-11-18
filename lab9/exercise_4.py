# You can assume that the first two arguments to rectangle() are
# integers at least equal to 0, and that the third argument, if any,
# is a string consisting of an uppercase letter.
#
# The rectangle is read by going down the first column (if it exists),
# up the second column (if it exists), down the third column (if it exists),
# up the fourth column  (if it exists)...
#
# Hint: ord() and chr() are useful.
# 65 - 90
import numpy as np
def rectangle(width, height, starting_from='A'):
    '''
    >>> rectangle(0, 0)
    >>> rectangle(10, 1, 'V')
    VWXYZABCDE
    >>> rectangle(1, 5, 'X')
    X
    Y
    Z
    A
    B
    >>> rectangle(10, 7)
    ANOBCPQDER
    BMPADORCFQ
    CLQZENSBGP
    DKRYFMTAHO
    EJSXGLUZIN
    FITWHKVYJM
    GHUVIJWXKL
    >>> rectangle(12, 4, 'O')
    OVWDELMTUBCJ
    PUXCFKNSVADI
    QTYBGJORWZEH
    RSZAHIPQXYFG
    '''
    # pass
    mtx=np.array([[' ' for _ in range(width)] for _ in range(height)])
    blanks=[]
    r1=range(height)
    r2=range(height-1,-1,-1)
    for i in range(width):
        if(i%2):
            r=r2
        else:
            r=r1
        for j in r:
            blanks.append((j,i))
    cur=ord(starting_from)
    for i in blanks:
        mtx[i[0],i[1]]=chr((cur-65)%26+65)
        cur+=1
    for i in mtx:
        for j in i:
            print(j,end='')
        print()
    # REPLACE PASS ABOVE WITH YOUR CODE
        

if __name__ == '__main__':
    # rectangle(12, 4, 'O')
    import doctest
    doctest.testmod()
