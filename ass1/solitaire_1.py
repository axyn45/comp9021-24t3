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

def play(deck,seedIn=0):
    def drawCards(deck):
        cards=[]
        for i in range(len(deck)-1,len(deck)-17,-1):
            cards.append(deck[i])
            del deck[i]
        return cards
    
    def displayCards(cards):
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
    seed(seedIn)
    shuffle(deck)
    ondesk=[]
    print(f'\nDrawing and placing {16-len(ondesk)} cards:')
    ondesk=drawCards(deck)
    print(']'*len(deck))
    displayCards(ondesk)
    picCount=putAside(ondesk)
    while(not picCount==0):
        print(f'\nPutting {picCount} {'pictures' if picCount>1 else 'picture'} aside:')
        picCount=putAside(ondesk)
        displayCards(ondesk)
        if(isWinning(len(deck)+len(ondesk)-picCount)==1): 
            print('\nYou uncovered all pictures, you won!')
            return True
        print(f'\nDrawing and placing {picCount} {'cards' if picCount>1 else 'card'}:')
        picCount=replaceCards(ondesk,deck)
        print(']'*len(deck))
        displayCards(ondesk)
    deck.extend(ondesk[::-1])
    if(isWinning(len(deck))==-1): 
            print(f'\nYou uncovered only {52-len(deck)} pictures, you lost!')
            return True
    
    global playedrounds
    playedrounds=playedrounds+1
    return False

def isWinning(leftcards):
    global playedrounds
    pct=52-leftcards
    if(pct==12):
        return 1
    elif(playedrounds==3): 
        return -1
    else: return 0


def game():
    
    seed_in=int(input('Please enter an integer to feed the seed() function: '))
    deck=list(range(52))
    print('\nDeck shuffled, ready to start!\n]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]')
    for i in range(4):
        match i:
            case 0:
                print('\nStarting first round...')
            case 1:
                print('\nAfter shuffling, starting second round...')
            case 2:
                print('\nAfter shuffling, starting third round...')
            case 3:
                print('\nAfter shuffling, starting fourth round...')
        if(play(deck,seed_in+i)): break

game()