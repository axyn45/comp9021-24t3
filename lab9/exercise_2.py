# You can assume that the argument L to positive_gaps()
# is a list of integers.
# 
# Records all gaps between two SUCCESSIVE members of L,
# say a and b, such that b is STRICTLY GREATER than a.
#
# Gap values are output from smallest to largest.
#
# For a given gap value, gaps for that value are output
# from smallest to largest starts of gap, without repetition,
# with 2 spaces before "Between".


from collections import defaultdict


def positive_gaps(L):
    '''
    >>> positive_gaps([])
    >>> positive_gaps([2, 2, 2, 1, 1, 0])
    >>> positive_gaps([0, 1, 1, 2, 2, 2])
    Gaps of 1:
      Between 0 and 1
      Between 1 and 2
    >>> positive_gaps([0, 4, 0, 4, 0, 4])
    Gaps of 4:
      Between 0 and 4
    >>> positive_gaps([2, 14, 1, 14, 19, 6, 4, 16, 3, 2])
    Gaps of 5:
      Between 14 and 19
    Gaps of 12:
      Between 2 and 14
      Between 4 and 16
    Gaps of 13:
      Between 1 and 14
    >>> positive_gaps([1, 3, 3, 0, 3, 0, 3, 7, 5, 0, 3, 6, 3, 1, 4])
    Gaps of 2:
      Between 1 and 3
    Gaps of 3:
      Between 0 and 3
      Between 1 and 4
      Between 3 and 6
    Gaps of 4:
      Between 3 and 7
    >>> positive_gaps([11, -10, -9, 11, 15, 8, -5])
    Gaps of 1:
      Between -10 and -9
    Gaps of 4:
      Between 11 and 15
    Gaps of 20:
      Between -9 and 11
    '''
    gaps={}
    for i in range(1,len(L)):
        gap=L[i]-L[i-1]
        if(gap>0):
            try:
              gaps[gap].add((L[i-1],L[i]))
            except KeyError:
              gaps[gap]={(L[i-1],L[i])}
    gaps={k:v for k,v in sorted(gaps.items(),key=lambda x:x[0])}
    for k,v in gaps.items():
      print(f'Gaps of {k}:')
      for i in v:
         print(f'  Between {i[0]} and {i[1]}')

    # pass
    # REPLACE PASS ABOVE WITH YOUR CODE
                

if __name__ == '__main__':
    # positive_gaps([11, -10, -9, 11, 15, 8, -5])
    import doctest
    doctest.testmod()
