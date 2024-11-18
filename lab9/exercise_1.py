# Note that NONE OF THE LINES THAT ARE OUTPUT HAS TRAILING SPACES.
#
# You can assume that vertical_bars() is called with nothing but
# integers at least equal to 0 as arguments (if any).

import numpy as np
def vertical_bars(*x):
    '''
    >>> vertical_bars()
    >>> vertical_bars(0, 0, 0)
    >>> vertical_bars(4)
    *
    *
    *
    *
    >>> vertical_bars(4, 4, 4)
    * * *
    * * *
    * * *
    * * *
    >>> vertical_bars(4, 0, 3, 1)
    *
    *   *
    *   *
    *   * *
    >>> vertical_bars(0, 1, 2, 3, 2, 1, 0, 0)
          *
        * * *
      * * * * *
    '''
    if(not x):
        return
    height=max(x)
    matrix=np.array([list(' '*len(x)) for _ in range(height)])
    if(height==0):
        return
    for i in range(len(x)):
        matrix[height-x[i]:,i]=list('*'*x[i])
    # print(matrix)
    for i in matrix:
        line=' '.join(i)
        
        print(line.rstrip())
    pass
    # REPLACE PASS ABOVE WITH YOUR CODE
                

if __name__ == '__main__':
    import doctest
    doctest.testmod()
