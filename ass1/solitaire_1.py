from itertools import chain
from random import seed, shuffle
from collections import defaultdict

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
        # print(']'*len(deck))
        # print(cards)
        # cardChrs=[card(i) for i in cards]
        for i in range(len(cards)):
            print(f'\t{card(cards[i])}',end='')
            if((i+1)%4==0):print()
    
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
    # print(seedIn)
    seed(seedIn)
    shuffle(deck)
    ondesk=[]
    print(f'\nDrawing and placing {16-len(ondesk)} cards:')
    ondesk=drawCards(deck)
    print(']'*len(deck))
    # print(ondesk)
    displayCards(ondesk)
    picCount=putAside(ondesk)
    # print(ondesk)
    while(not picCount==0):
        print(f'\nPutting {picCount} {'pictures' if picCount>1 else 'picture'} aside:')
        displayCards(ondesk)
        print(f'\nDrawing and placing {picCount} cards:')
        picCount=replaceCards(ondesk,deck)
        print(']'*len(deck))
        displayCards(ondesk)
    deck.extend(ondesk[::-1])


        




def game():
    def isWinning(r,deck):
        pct=52-len(deck)
        if(pct==12):
            print('\nYou uncovered all pictures, you won!')
            return True
        elif(r==3): 
            print(f'\nYou uncovered only {pct} pictures, you lost!')
            return False
        else: return False
    seed_in=int(input('Please enter an integer to feed the seed() function: '))
    # seed_in=0
    # print(type(seed_in))
    # seed(seed_in)
    deck=list(range(52))
    # shuffle(deck)
    # print(deck)
    # deck=deck[51:35:-1]
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
        play(deck,seed_in+i)
        # print(deck)
        if(isWinning(i,deck) or i==3): break
        # elif(i==3): 
    # play(deck,seed_in)
    # print('\nAfter shuffling, starting second round...')
    # if(52-len(deck)==12):
    #     print('\nYou uncovered all pictures, you won!')
    #     return
    # play(deck,seed_in+1)
    # print('\nAfter shuffling, starting third round...')

    # if(52-len(deck)==12):
    #     print('\nYou uncovered all pictures, you won!')
    #     return
    # play(deck,seed_in+2)
    # print('\nAfter shuffling, starting fourth round...')

    # if(52-len(deck)==12):
    #     print('\nYou uncovered all pictures, you won!')
    #     return
    # play(deck,seed_in+3)
    
    # print(52-len(deck))
    # print(deck)
    # for i in range(len(deck)):
    #     print(card(deck[i]),end='')

        # if i%8==0: print()
    # print('\nDeck shuffled, ready to start!\U0001F0A8')
    # print(']'*52)
    # print('\nStarting first round...')
    # print('Drawing and placing 16 cards:')
    # print(']'*(52-16))
# INSERT YOUR CODE HERE

# seed(0)
# a=list(range(52))
# shuffle(a)
# print(a,card(24))

game()
# print(card(25))
# if(isPicture(25)):print('yes')
# for i in list(range(52)):
#     if(isPicture(i)):
#         print(i,card(i),'yes')
