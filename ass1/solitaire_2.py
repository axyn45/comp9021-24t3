from itertools import chain
from random import seed, shuffle
from collections import defaultdict

# INSERT YOUR CODE HERE

# def card(n,returnIdx=False):
#     if(n==-1):return ''

#     lut=[0x1f0b0,0x1f0c0,0x1f0d0,0x1f0a0]
#     noffset=n%13+1 if n%13<11 else n%13+2
#     res=0
#     match n//13:
#         case 0:
#             res=lut[0]+noffset
#         case 1:
#             res=lut[1]+noffset
#         case 2:
#             res=lut[2]+noffset
#         case 3:
#             res=lut[3]+noffset
#     return res if returnIdx else chr(res)

def translateCard(n):
    return (n//13,n%13)

        
def play(seedIn,deck,desk):

    def drawCards(deck,hand):
        if(len(deck)==0):return hand
        newhand=deck[-min(3,len(deck)):]+hand
        for i in range(min(3,len(deck))):
            del deck[-1]
        return newhand

    deck.sort()
    seed(seedIn)
    shuffle(deck)
    print(deck)
    onfly=[]
    prevDeckLen=-1
    roundCount=0

    while(not len(deck)==prevDeckLen):
        roundCount=roundCount+1
        prevDeckLen=len(deck)
        while(not len(deck)==0):
            onfly=drawCards(deck,onfly)
            delist=[]
            for i in onfly:
                if(roundCount==3):
                    pass
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
                    if(roundCount==2):
                        print('D----',loc,i)
                    # onfly.remove(i)
                    delist.append(i)
                    print(i)
                else:
                    break
            for i in delist:
                onfly.remove(i)
            if(len(onfly)==0):
                break
        print(desk)
        # print(onfly[0],onfly[-3])
        deck.extend(onfly)
        onfly=[]
        if(prevDeckLen==len(deck)):
            break
        
    if(len(deck)!=0):
        print('Left:',len(deck))
    else:
        print('Win')



# a=[i for i in range(0,10,-1)]
# for i in a:
#     if(i%3==0):a.remove(i)
        

        

def game(seedin=None):
    if(seedin is None):
        seedIn=input('Please enter an integer to feed the seed() function: ')
    else: seedIn=seedin
    seedIn=int(seedIn)
    deck=list(range(52))
    desk=[[] for i in range(8)]
    # lastlen=0
    # while(not lastlen==len(deck)):
    #     play(seedIn=)
    play(seedIn,deck,desk)
    print(len(deck))
    # seed(seedIn)
    # shuffle(deck)


if __name__ == "__main__":
    # simulate(500,11)
    game(9)
