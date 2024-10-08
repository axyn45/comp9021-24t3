from itertools import chain
from random import seed, shuffle
from collections import defaultdict

# INSERT YOUR CODE HERE

def card(n,returnIdx=False):
    if(n==-1):return ''

    lut=[0x1f0b0,0x1f0c0,0x1f0d0,0x1f0a0]
    noffset=n%13+1 if n%13<11 else n%13+2
    res=0
    match n//13:
        case 0:
            res=lut[0]+noffset
        case 1:
            res=lut[1]+noffset
        case 2:
            res=lut[2]+noffset
        case 3:
            res=lut[3]+noffset
    return res if returnIdx else chr(res)

def translateCard(n):
    return (n//13,n%13)

        
def play(seedIn,deck,desk):
    def drawCards(deck,hand):
        if(len(deck)==0): return hand.append(-1)
        drawLen=min(3,len(deck))
        # hand.extend(deck[-drawLen:])
        newhand=deck[-drawLen:]+hand
        for i in range(drawLen):
            del deck[-1]
        # print('hand',hand)
        return newhand

    deck.sort()
    seed(seedIn)
    shuffle(deck)
    print(deck)
    onfly=[]

    while(not len(deck)==0):
        # if(drawCards(deck,onfly)==False): break
        onfly=drawCards(deck,onfly)
        
        for i in onfly:
            if(i==-1):break
            loc=-1
            coord=translateCard(i)
            if(coord[1]==0):
                loc=coord[0]%4
            elif(coord[1]==12):
                loc=4+coord[0]%4
            elif(len(desk[coord[0]%4]) and len(desk[4+coord[0]%4])):
                loc=coord[0]%4
            elif(len(desk[coord[0]%4]) and desk[coord[0]%4][-1]+1==coord[1]):
                loc=coord[0]%4
            elif(len(desk[4+coord[0]%4]) and desk[4+coord[0]%4][-1]+1==coord[1]):
                loc=4+coord[0]%4
            if(not loc==-1):
                desk[loc].append(i)
                onfly.remove(i)
            else:
                # print('bk',i)
                break
        print('-----------------------------')
        print(deck)
        print(onfly)
        print(desk)
        if(onfly[-1]==-1):break
    print(deck)
    print(desk)



# a=[i for i in range(0,10,-1)]
# for i in a:
#     if(i%3==0):a.remove(i)
        

        

def game(seedin=None):
    if(seedin is None):
        seedIn=input('Please enter an integer to feed the seed() function: ')
    else: seedIn=seedin
    deck=list(range(52))
    desk=[[] for i in range(8)]
    play(seedIn,deck,desk)
    # seed(seedIn)
    # shuffle(deck)


if __name__ == "__main__":
    # simulate(500,11)
    game()
