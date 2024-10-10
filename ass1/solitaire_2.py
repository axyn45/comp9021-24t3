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

        
def play(seedIn,deck,desk,mute=False):

    def drawCards(deck,hand):
        if(len(deck)==0):return hand
        newhand=deck[-min(3,len(deck)):]+hand
        for i in range(min(3,len(deck))):
            del deck[-1]
        return newhand
    # a=12
    output=[]

    def lprint(string=''):
        if(mute):
            return
        splits=[i.rstrip() for i in string.split('\n')]
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
            line=line+('['*(len(desk[i])-1)+(card(desk[i][-1]) if len(desk[i]) else '')).ljust(15)
            if(i==3):
                line=line+'\n    '
        lprint(line)
        lprint()
        
             
    deck.sort()
    seed(seedIn)
    shuffle(deck)
    onfly=[]
    prevDeckLen=-1
    roundCount=0
    
    lprint('Deck shuffled, ready to start!')
    # lprint(']'*len(deck))
    printPiles(deck,onfly)
    
    while(not len(deck)==prevDeckLen):
        roundCount=roundCount+1
        if(len(deck)+len(onfly)==0):break
        lprint(f'Starting to draw 3 cards (if possible) again and again for the {orderConversion(roundCount)} time...\n')
        prevDeckLen=len(deck)
        while(not len(deck)==0):
            onfly=drawCards(deck,onfly)
            printPiles(deck,onfly)
            printDesk(desk)
            # delist=[]
            onflyCopy=onfly[::1]
            for i in onflyCopy:
                loc=None
                coord=translateCard(i)
                if(coord[1]==0):
                    loc=coord[0]%4
                    lprint('Placing one of the base cards!')
                elif(coord[1]==12):
                    loc=4+coord[0]%4
                    lprint('Placing one of the base cards!')
                elif(len(desk[coord[0]%4])>0 and i==desk[coord[0]%4][-1]+1):
                    loc=coord[0]%4
                    lprint('Making progress on an increasing sequence!')
                elif(len(desk[4+coord[0]%4])>0 and i==desk[4+coord[0]%4][-1]-1):
                    loc=4+coord[0]%4
                    lprint('Making progress on a decreasing sequence!')
                if(not loc==None):
                    desk[loc].append(i)
                    # delist.append(i)
                    onfly.remove(i)
                    
                    printPiles(deck,onfly)
                    printDesk(desk)
                    # print(i)
                else:
                    break
            # for i in delist[::-1]:
            #     onfly.remove(i)
                
            # if(len(onfly)==0):
            #     break
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

def game(seedin=None,mute=False):
    if(seedin is None):
        seedIn=input('Please enter an integer to feed the seed() function: ')
    else: seedIn=seedin
    seedIn=int(seedIn)
    deck=list(range(52))
    desk=[[] for i in range(8)]
    collection=[]
    result=False
    result,collection=play(seedIn,deck,desk)
    if(mute):
        return len(deck)
    del collection[-1]
    if(result):
        print('\nAll cards have been placed, you won!')
    else:
        print(f'\n{len(deck)} cards could not be placed, you lost!')

    print(f'\nThere are {len(collection)} lines of output; what do you want me to do?')
    while True:
        option=input(f'\nEnter: q to quit\n       a last line number (between 1 and {len(collection)})\n       a first line number (between -1 and -{len(collection)})\n       a range of line numbers (of the form m--n with 1 <= m <= n <= {len(collection)})\n       ')
        if(option=='q'):return
        try:
            option=[i.strip() for i in option.split('--')]
            # if()
            for i in option:
                if not (47<ord(i[0])<58 or ord(i[0])==45):
                    raise Exception
            option=[int(i) for i in option]
                
        except:
            continue
        if(len(option)==2 and (1<=option[0]<=option[1]<=len(collection))):
            print()
            for i in collection[option[0]-1:option[1]]:
                print(i)
        elif(len(option)==1):
            if(1<=option[0]<=len(collection)):
                print()
                for i in collection[:option[0]]:
                    print(i)
            elif(-1>=option[0]>=-len(collection)):
                print()
                for i in collection[option[0]:]:
                    print(i)
            else:
                return
            

def simulate(n,i):
    # print(n,i)
    lut={}
    for j in range(n):
        result=game(i+j,True)
        # print(j,result,'-----------------------------------------------------------')
        lut[result]=1 if(result not in lut) else lut[result]+1
    print('Number of cards left | Frequency\n--------------------------------')
    # lut=sorted(lut)
    # print(lut)

    for k in sorted(lut)[::-1]:
        print(str(k).rjust(20),'|',f'{lut[k]/n*100:,.2f}%'.rjust(9))


if __name__ == "__main__":
    # simulate(500,11)
    game()
