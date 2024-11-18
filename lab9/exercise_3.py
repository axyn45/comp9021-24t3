# You can assume that the argument to solve() is of the form
# x+y=z where:
# - x, y and z are NONEMPTY sequences of UNDERSCORES and DIGITS;
# - there can be any number of spaces (possibly none) before x,
#   between x and +, between + and y, between y and =, between = and z,
#   and after z.
#
# ALL OCCURRENCES OF _ ARE MEANT TO BE REPLACED BY THE SAME DIGIT.
#
# Note that sequences of digits such as 000 and 00037 represent
# 0 and 37, consistently with what int('000') and int('00037') return,
# respectively.
#
# When there is more than one solution, solutions are output from
# smallest to largest values of _.
#
# Note that an equation is always output with a single space before and after
# + and =, with no leading nor trailing spaces, and without extra leading 0s
# in front of an integer.
#
# Hint: The earlier you process underscores, the easier,
#       and recall what dir(str) can do for you.


def solve(equation):
    '''
    >>> solve('1 + 2 = 4')
    No solution!
    >>> solve('123 + 2_4 = 388')
    No solution!
    >>> solve('1+2   =   3')
    1 + 2 = 3
    >>> solve('123 + 2_4 = 387')
    123 + 264 = 387
    >>> solve('_23+234=__257')
    23 + 234 = 257
    >>> solve('   __   +  _____   =     ___    ')
    0 + 0 = 0
    >>> solve('__ + __  = 22')
    11 + 11 = 22
    >>> solve('   012+021   =   00__   ')
    12 + 21 = 33
    >>> solve('_1   +    2   =    __')
    31 + 2 = 33
    >>> solve('0 + _ = _')
    0 + 0 = 0
    0 + 1 = 1
    0 + 2 = 2
    0 + 3 = 3
    0 + 4 = 4
    0 + 5 = 5
    0 + 6 = 6
    0 + 7 = 7
    0 + 8 = 8
    0 + 9 = 9
    '''
    class numObj:
        def __init__(self,raw) -> None:
            self.raw=raw
            self.sum=0
            self.uksum=0
            mul=1
            for i in raw[::-1]:
                if(i=='_'):
                    self.uksum+=mul
                else:
                    self.sum+=mul*int(i)
                mul*=10
        def testN(self,n):
            return self.sum+self.uksum*n
        def getStrWithN(self,n):
            res=self.raw.replace('_',str(n)).lstrip('0').lstrip('0')
            return res if(res) else '0'

    nospace=equation.replace(' ','')
    a,b=nospace.split('+')
    b,c=b.split('=')
    a=numObj(a)
    b=numObj(b)
    c=numObj(c)
    res=[]
    if(a.uksum==b.uksum==c.uksum==0):
        if(a.sum+b.sum==c.sum):
            res.append(0)
    else:
        for i in range(10):
            if(a.testN(i)+b.testN(i)==c.testN(i)):
                res.append(i)
    if(not res):
        print('No solution!')
    for i in res:
        print(f'{a.getStrWithN(i)} + {b.getStrWithN(i)} = {c.getStrWithN(i)}')
    pass
    # REPLACE PASS ABOVE WITH YOUR CODE
        

if __name__ == '__main__':
    # solve('123 + 2_4 = 388')
    import doctest
    doctest.testmod()
