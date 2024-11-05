# EDIT THE FILE WITH YOUR SOLUTION
import re
import numpy as np
import copy
from itertools import tee
import time
from collections import OrderedDict

class Crossword:
    def __init__(self,filename) -> None:
        # print(filename)
        self.rawtex=[]
        self.tex=''
        self.blackcount=0
        self.lettercount=0
        vwords=[]
        hwords=[]
        self.letterscount=0
        self.debug=0

        # with open('ass2/dictionary.txt','r') as d:
        #     self.dictionary=np.array(list(d))

        with open(filename,'r') as f:
            for l in f:
                self.rawtex.append(l)
                self.tex+=l.split('%')[0].replace(' ','').strip()

        matches=re.findall(r'(?<=\\begin{crossgrid}\[)[hv=,\d]*(?=])',self.tex)
        if(len(matches)):
            matches=matches[0].split(',')
            self.width=int(matches[0].split('=')[1])
            self.height=int(matches[1].split('=')[1])
        else:
            matches=re.findall(r'(?<=\\gridcross\{)[A-Z,\*]*(?=})',self.tex)
            mstr=matches[0].split(',')
            self.width=len(mstr[0])
            self.height=len(mstr)


        matches=re.findall(r'(?<=\\blackcases{)[\d\/,]*(?=})',self.tex)
        if(len(matches)):
            blackcases=[]
            matches=matches[0].split(',')
            for i in matches:
                coord=i.split('/')
                blackcases.append((int(coord[1])-1,int(coord[0])-1))
        
        matches=re.findall(r'(?<=\\words\[v\]{)[\d\/,a-zA-Z]*(?=})',self.tex)
        if(len(matches)):
            matches=matches[0].split(',')
            for i in matches:
                coord=i.split('/')
                vwords.append((int(coord[1])-1,int(coord[0])-1,coord[2]))

        matches=re.findall(r'(?<=\\words\[h\]{)[\d\/,a-zA-Z]*(?=})',self.tex)
        if(len(matches)):
            matches=matches[0].split(',')
            for i in matches:
                coord=i.split('/')
                hwords.append((int(coord[1])-1,int(coord[0])-1,coord[2]))

        for i in vwords+hwords:
            self.letterscount+=len(i[2])

        self.grid=np.array([[' ' for _ in range(self.width)] for _ in range(self.height)])
        
        if('mstr' in locals()):
            for i in range(len(mstr)):
                self.grid[i]=list(mstr[i])
        else:
            if('blackcases' in locals()):
                for i in blackcases:
                    self.grid[i[0],i[1]]='*'

            if('vwords' in locals()): 
                for i in vwords:
                    self.grid[i[0]:i[0]+len(i[2]),i[1]]=list(i[2])

            if('hwords' in locals()):
                for i in hwords:
                    self.grid[i[0],i[1]:i[1]+len(i[2])]=list(i[2])
        for i in self.grid:
            for j in range(i.size):
                if(i[j]=='*'):
                    self.blackcount+=1
                elif(not i[j]==''):
                    self.lettercount+=1
        self.splitSlots()

        self.matchCache={}
    
    def __str__(self):
        # ctV=0
        # ctH=0
        # for i in self.grid.T:
        #     notcomplete=False
        #     for j in range(len(i)):
        #         if(i[j]==' ' or ('*'==i[j] and (j==0 or i[j-1]==i[j]))):
        #             notcomplete=True
        #         if(i[j]=='*' or j==len(i)-1):
        #             if(not notcomplete):
        #                 ctV+=1
        #             notcomplete=False
        # for i in self.grid:
        #     notcomplete=False
        #     for j in range(len(i)):
        #         if(i[j]==' ' or ('*'==i[j] and (j==0 or i[j-1]==i[j]))):
        #             notcomplete=True
        #         if(i[j]=='*' or j==len(i)-1):
        #             if(not notcomplete):
        #                 ctH+=1
        #             notcomplete=False
        # print(self.grid)
        countH=0
        countV=0
        letters=0
        for i in self.hSlots:
            temp=self.slot2str(i)
            if(' ' not in temp):
                countH+=1
            letters+=len(temp.replace(' ',''))
        for i in self.vSlots:
            temp=self.slot2str(i)
            if(' ' not in temp):
                countV+=1
            # letters+=len(temp.replace(' ',''))
        return (f'A grid of width {self.width} and height {self.height}, with {self.blackcount if self.blackcount else "no"} blackcase{"" if self.blackcount==1 else "s"}, filled with {letters if letters else "no"} letter{"" if letters==1 else "s"},\nwith {countV if countV else "no"} complete vertical word{"" if countV==1 else "s"} and {countH if countH else "no"} complete horizontal word{"" if countH==1 else "s"}.')
        
    def filterPrefix(prefix,words):
        result=[]
        for w in words:
            if(w.startswith(prefix)):
                result.append(w)
        return result
    
    def splitSlots(self):
        # result=[]
        self.hSlots=[]
        self.vSlots=[]
        # self.nhSlots={}
        # self.nvSlots={}
        # self.sortedHSlots=[]
        # self.sortedVSlots=[]
        # self.sortedSlots=[]
        self.slots={}
        self.hslots={}
        self.vslots={}

        # self.sslots={}
        self.slotsKeys=[]
        self.hslotsKeys=[]
        self.hSlotLut={}
        self.vSlotLut={}

        # self.
        def parseHorizontal(i):
            startpos=0
            for j in range(self.grid[i].size+1):
                if(j==self.grid[i].size or self.grid[i,j]=='*'):
                    if(not startpos==j and j-startpos>1):
                        self.slots[('h',(i,startpos))]=self.grid[i,startpos:j]
                        self.hslots[('h',(i,startpos))]=self.grid[i,startpos:j]
                        for k in range(startpos,j):
                            self.hSlotLut[(i,k)]=('h',(i,startpos))
                    startpos=j+1
        def parseVertical(i):
            startpos=0
            for j in range(self.grid.T[i].size+1):
                if(j==self.grid.T[i].size or self.grid.T[i,j]=='*'):
                    if(not startpos==j and j-startpos>1):
                        self.slots[('v',(startpos,i))]=self.grid.T[i,startpos:j]
                        self.vslots[('v',(startpos,i))]=self.grid.T[i,startpos:j]
                        for k in range(startpos,j):
                            self.vSlotLut[(k,i)]=('v',(startpos,i))
                    startpos=j+1
        for i in range(self.width):
            parseHorizontal(i)
            parseVertical(i)
        
        for i in range(self.height):
            startpos=0
            for j in range(self.grid[i].size+1):
                if(j==self.grid[i].size or self.grid[i,j]=='*'):
                    if(not startpos==j and j-startpos>1):
                        self.hSlots.append(self.grid[i,startpos:j])
                        # self.nhSlots[('h',(i,startpos))]=self.grid[i,startpos:j]
                    startpos=j+1
        
        for i in range(self.width):
            startpos=0
            for j in range(self.grid.T[i].size+1):
                if(j==self.grid.T[i].size or self.grid.T[i,j]=='*'):
                    if(not startpos==j and j-startpos>1):
                        self.vSlots.append(self.grid.T[i,startpos:j])
                        # self.nvSlots[('v',(i,startpos))]=self.grid.T[i,startpos:j]
                    startpos=j+1
        # self.sortedHSlots=sorted(self.hSlots,key=lambda x:x.size)
        # self.sortedVSlots=sorted(self.vSlots,key=lambda x:x.size)
        # self.sortedSlots=sorted(self.sortedHSlots+self.sortedVSlots,key=lambda x:x.size)
        # self.nhSlots={k: v for k, v in sorted(self.nhSlots.items(),key=lambda x:x[1].size)}
        # self.nvSlots={k: v for k, v in sorted(self.nvSlots.items(),key=lambda x:x[1].size)}
        
        # self.slots={**self.nhSlots,**self.nvSlots}
        # self.slots=self.sslots
        # for i in self.slots.keys():
        #     self.slotsKeys.append(i)
        for i in self.slots.keys():
            self.slotsKeys.append(i)

        for i in self.hslots.keys():
            self.hslotsKeys.append(i)
        # pass

    def clearGrid(self):
        for i in range(self.height):
            for j in range(self.width):
                if(not (self.grid[i,j]==' ' or self.grid[i,j]=='*')):
                    self.grid[i,j]=' '
                    
    def initWordsByLen(self):
        if(not hasattr(self,'wordsbylen')):
            self.wordsbylen={}
        validLengths=set([v.size for k,v in self.slots.items()])
        for length in validLengths:
            if(length in self.wordsbylen):
                return
            self.wordsbylen[length]=[]
            for word in self.words:
                if(len(word)==length):
                    self.wordsbylen[length].append(word)
        # if(not hasattr(self,'wordslongbylen')):
        #     self.wordslongbylen={}
        #     for k,v in self.wordsbylen.items():
        #         self.wordslongbylen[k]=' '.join(v)
    
    def loadWords(self,filename):
        if(not hasattr(self,'hSlots') or not hasattr(self,'vSlots')):
            self.splitSlots()

        if(not hasattr(self,'trieDict')):
            self.trieDict={}
        
        words=[]
        validLengths=set([v.size for k,v in self.slots.items()])
        with open(filename,'r') as f:
            for i in f:
                i=i.strip()
                if(len(i) in validLengths):
                    words.append(i)
        self.words=np.array(words)

        self.initWordsByLen()
        for length,wordList in self.wordsbylen.items():
            self.trieDict[length]={}

            for i in range(len(wordList)):
                anchor=self.trieDict[length]
                for j in range(len(wordList[i])):
                    # anchor=j
                    if(wordList[i][j] not in anchor):
                        if(j==len(wordList[i])-1):
                            anchor[wordList[i][j]]=self.slot2str(wordList[i])
                        else:
                            anchor[wordList[i][j]]={}
                    anchor=anchor[wordList[i][j]]
        self.generateWordTries()
        # print(self.validateVertical())
        # try:
        #     print(self.trieDict[3]['A']['X']['N'])
        # except KeyError:
        #     print('no such word')
        pass

    def trieMatch(self,trieIdx,pattern,trie=None,isRoot=True,):
        if(pattern and (not pattern.strip())):
            return True
        if(isRoot):
            trie=self.slotTries[trieIdx]
            if(trieIdx in self.matchCache):
                if(pattern in self.matchCache[trieIdx]):
                    # pass
                    return self.matchCache[trieIdx][pattern]
                else:
                    self.matchCache[trieIdx][pattern]=False
            else:
                self.matchCache[trieIdx]={}
                self.matchCache[trieIdx][pattern]=False

        if(isinstance(trie,str)):
            if(not pattern):
                return True
            else:
                return False
        elif(pattern[0] in trie):
            result=self.trieMatch(trieIdx,pattern[1:],trie[pattern[0]],False)
            if(isRoot):
                self.matchCache[trieIdx][pattern]=result
            return result
        elif(pattern[0]==' '):
            result=False
            for k,v in trie.items():
                result|=self.trieMatch(trieIdx,pattern[1:],v,False)
                if(result):
                    break
            if(isRoot):
                self.matchCache[trieIdx][pattern]=result
            return result
        else:
            # if(isRoot):
            #     self.matchCache[trieIdx][pattern]=False
            return False

    def validateVertical(self,key):
        # return True
        for i in range(key[1][1],key[1][1]+self.slots[key].size):
            vkey=(key[1][0],i)
            pattern=self.slot2str(self.slots[self.vSlotLut[vkey]])
            if(not self.trieMatch(self.vSlotLut[vkey],pattern)):
                return False
        return True
    
    def validateHorizontal(self,key):
        # return True
        for i in range(key[1][0],key[1][0]+self.slots[key].size):
            hkey=('h',(i,key[1][1]))
            pattern=self.slot2str(self.slots[self.hSlotLut[(hkey[1])]])
            if(not self.trieMatch(self.hSlotLut[(hkey[1])],pattern)):
                return False
        return True
                

    def isSolved(self):
        for k,v in self.slots.items():
            pattern=self.slot2str(v)
            if(' ' in pattern or not self.trieMatch(k,pattern)):
                return False
        return True

    def slot2str(self,slot):
        result=''
        for i in slot:
            result+=i
        return result

    def reduceTrie(self,prevAnchor,idx,pattern):
        if(isinstance(prevAnchor[idx],str) and not pattern):
            return True
        result=False
        for k,v in prevAnchor[idx].copy().items():
            if(k!=pattern[0] and not pattern[0]==' '):
                del prevAnchor[idx][k]
                pass
            else:
                result|=self.reduceTrie(prevAnchor[idx],k,pattern[1:] if len(pattern)>1 else '')
        if(not result):
            del prevAnchor[idx]
        return result

    def generateWordTries(self):
        if(not hasattr(self,'slotTries')):
            self.slotTries={}
        for k,v in self.slots.items():
            slotstr=self.slot2str(self.slots[k])
            if(' ' not in slotstr):
                self.slotTries[k]=self.word2trie(slotstr)
                continue
            self.slotTries[k]=copy.deepcopy(self.trieDict[len(slotstr)])
            if(not slotstr.strip()):
                continue
            self.reduceTrie(self.slotTries,k,slotstr)
        
        for k,v in self.slots.items():
            slotstr=self.slot2str(self.slots[k])
            if(' ' not in slotstr):
                self.slotTries[k]=self.word2trie(slotstr)
                continue
            self.slotTries[k]=copy.deepcopy(self.trieDict[len(slotstr)])
            if(not slotstr.strip()):
                continue
            self.reduceTrie(self.slotTries,k,slotstr)
        # a=self.enumTrie(self.slotTries[('h',(0,5))])
        # for i in a:
        #     print(i,end=' ')
        #     pass
        self.candidates={}
        for k,v in self.slots.items():
            x=None
            self.candidates[k],x=tee(self.enumTrie(self.slotTries[k]))
        pass
        

    def word2trie(self,word,pos=0):
        if(len(word)==pos):
            return word
        return {word[pos]:self.word2trie(word,pos+1)}
    
    def enumTrie(self,trie):
        if(isinstance(trie,str)):
            yield trie
        else:
            for k,v in trie.items():
                yield from self.enumTrie(v)

    # def listTrie(self,trie):
    #     result=[]
    #     if(isinstance(trie,str)):
    #         result.append(trie)
    #     else:
    #         for k,v in trie.items():
    #             result+=self.listTrie(v)
        # yield None
    # def enumTrieFrom(self,trie,word,idx):
    #     if(isinstance(trie,str)):
    #         yield trie
    #     else:
    #         for k,v in trie.items():
    #             if()
    #             yield from self.enumTrie(v)

    def fitNextWord(self,slotIdx,iterObj):
        pattern=self.slot2str(self.hslots[slotIdx])
        iterObj,backup=tee(iterObj)
        for word in backup:
            if(self.debug%100000==0):
                print(self.debug,slotIdx,word,end='\t\t')
                for k,v in self.hslots.items():
                    print(self.slot2str(v),end=' ')
                print()
            self.debug+=1
            if(not self.trieMatch(slotIdx,pattern)):
                continue
            
                # return True
            self.hslots[slotIdx][:]=list(word)
            isValid=self.validateVertical(slotIdx) #if slotIdx[0]=='h' else self.validateHorizontal(slotIdx)
            if(isValid):
                # if(self.slots[slotIdx].size==len(word)):
                #     return True
                self.steptracks.append((slotIdx,pattern,backup))
                return True
            else:
                self.hslots[slotIdx][:]=list(pattern)
        return False
    
    def backtrack(self,idx,iterObj):
        if(not idx):
            return True
        if(self.fitNextWord(idx,iterObj)):
            if(self.hslotsKeys.index(idx)>=len(self.hslots)-1):
                return self.backtrack(0,None)
            nextKey=self.hslotsKeys[self.hslotsKeys.index(idx)+1]
            return self.backtrack(nextKey,self.candidates[nextKey])
        return False

    def placeWords(self):
        self.debug=0
        if(not hasattr(self,'steptracks')):
            self.steptracks=[]  # e=(pos:int; prevstate:string; newstate:string)
        if(self.isSolved()):
            return True
        slotIdx=self.hslotsKeys[0]
        prevWord=self.candidates[slotIdx]
        while(not self.backtrack(slotIdx,prevWord)):
            if(not len(self.steptracks)):
                return False
            lastStep=self.steptracks[-1]
            self.slots[lastStep[0]][:]=list(lastStep[1])
            prevWord=lastStep[2]
            slotIdx=lastStep[0]
            del self.steptracks[-1]
        # print(self.grid)
        return True

    def fill_with_given_words(self,wordsfile,texfile):
        # self.splitSlots()
        
        
        self.loadWords(wordsfile)
        self.initWordsByLen()
        a=self.enumTrie(self.slotTries[self.slotsKeys[0]])
        for i in a:
            print(i,end=' ')
        print()
        if(self.placeWords()):
            print(f"I filled it!\nResult captured in filled_{texfile}")
        else:
            print("Hey, it can't be filled with these words!")
        return

    def solve(self,texfile,dictfile='dictionary.txt'):
        start_time = time.time()
        self.loadWords(dictfile)
        self.initWordsByLen()
        # a=self.enumTrie(self.slotTries[self.slotsKeys[0]])
        # for i in a:
        #     print(i,end=' ')
        # print()
        if(self.placeWords()):
            print(f"I solved it!\nResult captured in solved_{texfile}")
        else:
            print("Hey, it can't be solved!")
        print(self.grid)
        end_time = time.time()
        print(end_time-start_time,'secs')
        return


# count=0
if __name__=='__main__':
    a=Crossword('ass2/empty_grid_2.tex')
    print(a)
    a.solve('tete',dictfile='ass2/dictionary.txt')
    # a.fill_with_given_words('ass2/words_1.txt','test.tex')
    # print(a.splitArray)


