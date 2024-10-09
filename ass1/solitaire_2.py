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
        if(len(deck)==0):return hand
        newhand=deck[-min(3,len(deck)):]+hand
        for i in range(min(3,len(deck))):
            del deck[-1]
        return newhand
    # a=12
    output=[]

    def lprint(string=''):
        splits=string.split('\n')
        output.extend(splits)
    def orderConversion(n):
        match n:
            case 1:
                return 'first'
            case 2:
                return 'second'
            case 3:
                return 'third'
            case _:
                return str(n)+'th'
    def printPiles(deck,hand):
        lprint(']'*len(deck))
        if(len(hand)):
            lprint('['*(len(hand)-1)+card(hand[0]))
        else:
            lprint()
    def printDesk(desk):
        line='    '
        for i in range(8):
            line=line+'['*(len(desk[i])-1)+(card[desk[i][-1]] if len(desk[i]) else '').ljust(15)

        lprint()
        pass
             
    deck.sort()
    seed(seedIn)
    shuffle(deck)
    onfly=[]
    prevDeckLen=-1
    roundCount=0
    
    lprint('Deck shuffled, ready to start!')
    lprint(']'*len(deck))
    
    while(not len(deck)==prevDeckLen):
        roundCount=roundCount+1
        lprint(f'\nStarting to draw 3 cards (if possible) again and again for the {orderConversion(roundCount)} time...')
        prevDeckLen=len(deck)
        while(not len(deck)==0):
            onfly=drawCards(deck,onfly)
            printPiles(deck,onfly)
            delist=[]
            onflyCopy=onfly[::1]
            for i in onflyCopy:
                loc=None
                coord=translateCard(i)
                if(coord[1]==0):
                    loc=coord[0]%4
                elif(coord[1]==12):
                    loc=4+coord[0]%4
                elif(len(desk[coord[0]%4])>0 and i==desk[coord[0]%4][-1]+1):
                    loc=coord[0]%4
                elif(len(desk[4+coord[0]%4])>0 and i==desk[4+coord[0]%4][-1]-1):
                    loc=4+coord[0]%4
                if(not loc==None):
                    desk[loc].append(i)
                    # delist.append(i)
                    onfly.remove(i)
                    lprint('Placing one of the base cards!')
                    printPiles(deck,onfly)
                    # print(i)
                else:
                    break
            # for i in delist[::-1]:
            #     onfly.remove(i)
                
            if(len(onfly)==0):
                break
        # print(desk)
        deck.extend(onfly)
        onfly=[]
        if(prevDeckLen==len(deck)):
            break
        
    if(len(deck)!=0):
        result=False
    else:
        result=True
    return result,output

def game(seedin=None):
    if(seedin is None):
        seedIn=input('Please enter an integer to feed the seed() function: ')
    else: seedIn=seedin
    seedIn=int(seedIn)
    deck=list(range(52))
    desk=[[] for i in range(8)]
    collection=[]
    result=False
    result,collection=play(seedIn,deck,desk)

    if(result):
        print('\nAll cards have been placed, you won!')
    else:
        print(f'\n{len(deck)} cards could not be placed, you lost!')
    # print(result,len(deck))

if __name__ == "__main__":
    # simulate(500,11)
    game(0)
