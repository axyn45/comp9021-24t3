from itertools import chain
from random import seed, shuffle
from collections import defaultdict

playedrounds=0

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

def isPicture(n):
    return True if n%13>9 else False

def play(deck,seedIn=0,mute=False):
    def drawCards(deck):
        cards=[]
        for i in range(len(deck)-1,len(deck)-17,-1):
            cards.append(deck[i])
            del deck[i]
        return cards
    
    def displayCards(cards,mute=False):
        if(mute):return
        line=''
        for i in range(len(cards)):
            line=line+f'\t{card(cards[i])}'
            # print(f'\t{card(cards[i])}',end='')
            if((i+1)%4==0):
                print(line.rstrip())
                line=''
    
    def putAside(cards):
        ct=0
        for i in range(len(cards)):
            if(isPicture(cards[i])):
                cards[i]=-1
                ct=ct+1
        return ct
    
    def replaceCards(cards,deck):
        ct=0
        for i in range(len(cards)):
            if(cards[i]==-1):
                cards[i]=deck[-1]
                if(isPicture(cards[i])):ct=ct+1
                del deck[-1]
        return ct
    deck.sort()
    # print('----',seedIn)
    seed(seedIn)
    shuffle(deck)
    ondesk=[]
    myprint(f'\nDrawing and placing {16-len(ondesk)} cards:',mute)
    ondesk=drawCards(deck)
    myprint(']'*len(deck),mute)
    displayCards(ondesk,mute)
    picCount=putAside(ondesk)
    while(not picCount==0):
        myprint(f'\nPutting {picCount} {'pictures' if picCount>1 else 'picture'} aside:',mute)
        picCount=putAside(ondesk)
        displayCards(ondesk,mute)
        if(isWinning(len(deck)+len(ondesk)-picCount)==1): 
            myprint('\nYou uncovered all pictures, you won!',mute)
            return 12
        myprint(f'\nDrawing and placing {picCount} {'cards' if picCount>1 else 'card'}:',mute)
        picCount=replaceCards(ondesk,deck)
        myprint(']'*len(deck),mute)
        displayCards(ondesk,mute)
    deck.extend(ondesk[::-1])
    if(isWinning(len(deck))==-1): 
            myprint(f'\nYou uncovered only {52-len(deck)} pictures, you lost!',mute)
            return 52-len(deck)
    
    increRounds()
    return -1

def isWinning(leftcards):
    global playedrounds
    pct=52-leftcards
    if(pct==12):
        return 1
    elif(playedrounds==3): 
        return -1
    else: return 0

def myprint(str,mute=False,myend='\n'):
    if(not mute):
        print(str,end=myend)

def increRounds():
    global playedrounds
    playedrounds=playedrounds+1

def resetRounds():
    global playedrounds
    playedrounds=0

def game(seedparam=None,mute=False):
    
    if(seedparam==None):seed_in=int(input('Please enter an integer to feed the seed() function: '))
    else:seed_in=int(seedparam)
    deck=list(range(52))
    myprint('\nDeck shuffled, ready to start!\n]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]',mute)
    for i in range(4):
        match i:
            case 0:
                myprint('\nStarting first round...',mute)
            case 1:
                myprint('\nAfter shuffling, starting second round...',mute)
            case 2:
                myprint('\nAfter shuffling, starting third round...',mute)
            case 3:
                myprint('\nAfter shuffling, starting fourth round...',mute)
        # if(): return 0
        result=play(deck,seed_in+i,mute)
        if(result!=-1):
            resetRounds()
            return result

def simulate(n,i):
    # print(n,i)
    lut={}
    for j in range(n):
        result=game(i+j,True)
        # print(j,result,'-----------------------------------------------------------')
        lut[result]=1 if(result not in lut) else lut[result]+1
    print('Number of uncovered pictures | Frequency\n----------------------------------------')
    # lut=sorted(lut)
    # print(lut)

    for k in sorted(lut):
        print(str(k).rjust(28),'|',f'{lut[k]/n*100:,.2f}%'.rjust(9))


if __name__ == "__main__":
    # simulate(500,11)
    game()
    # print(game())