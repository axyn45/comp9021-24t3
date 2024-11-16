# EDIT THE FILE WITH YOUR SOLUTION
import re
import numpy as np
import copy
from itertools import tee
import time

class Crossword:
    def __init__(self,filename) -> None:
        self.rawtex=[]
        self.tex=''
        self.blackcount=0
        self.lettercount=0
        vwords=[]
        hwords=[]
        self.letterscount=0
        self.matchCache={}
        self.wordTrie={}
        self.debug=0
        self.blanks={}
        self.intersectionCache={}

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
        self.gridbackup=copy.deepcopy(self.grid)
        self.splitSlots()

        self.matchCache={}
        self.trieCache={}
    
    def __str__(self):
        countH=0
        countV=0
        letters=0
        for k,v in self.hslots.items():
            temp=self.slot2str(v)
            if(' ' not in temp):
                countH+=1
            letters+=len(temp.replace(' ',''))
        for k,v in self.vslots.items():
            temp=self.slot2str(v)
            if(' ' not in temp):
                countV+=1
        return (f'A grid of width {self.width} and height {self.height}, with {self.blackcount if self.blackcount else "no"} blackcase{"" if self.blackcount==1 else "s"}, filled with {letters if letters else "no"} letter{"" if letters==1 else "s"},\nwith {countV if countV else "no"} complete vertical word{"" if countV==1 else "s"} and {countH if countH else "no"} complete horizontal word{"" if countH==1 else "s"}.')

    
    def splitSlots(self):
        self.slots={}
        self.hslots={}
        self.vslots={}

        self.hslotsKeys=[]
        self.vslotsKeys=[]

        self.hSlotLut={}
        self.vSlotLut={}

        def parseHorizontal(i):
            startpos=0
            for j in range(self.grid[i].size+1):
                if(j==self.grid[i].size or self.grid[i,j]=='*'):
                    if(not startpos==j and j-startpos>=1):
                        self.slots[('h',(i,startpos))]=self.grid[i,startpos:j]
                        # self.slotsbackup[('h',(i,startpos))]=self.gridbackup[i,startpos:j]
                        self.hslots[('h',(i,startpos))]=self.grid[i,startpos:j]
                        for k in range(startpos,j):
                            self.hSlotLut[(i,k)]=('h',(i,startpos))
                    startpos=j+1
        def parseVertical(i):
            startpos=0
            for j in range(self.grid.T[i].size+1):
                if(j==self.grid.T[i].size or self.grid.T[i,j]=='*'):
                    if(not startpos==j and j-startpos>=1):
                        self.slots[('v',(startpos,i))]=self.grid.T[i,startpos:j]
                        # self.slotsbackup[('v',(startpos,i))]=self.gridbackup.T[i,startpos:j]
                        self.vslots[('v',(startpos,i))]=self.grid.T[i,startpos:j]
                        for k in range(startpos,j):
                            self.vSlotLut[(k,i)]=('v',(startpos,i))
                    startpos=j+1
        for i in range(self.width):
            parseHorizontal(i)
            parseVertical(i)
        
        
        for i in self.hslots.keys():
            self.hslotsKeys.append(i)
        for i in self.vslots.keys():
            self.vslotsKeys.append(i)

        hblanks={}
        vblanks={}
        for i in range(self.height):
            for j in range(self.width):
                if(not self.grid[i][j].strip()):
                    hblanks[i,j]=self.grid[i,j]
        for i in range(self.width):
            for j in range(self.height):
                if(not self.grid[j][i].strip()):
                    vblanks[j,i]=self.grid[j,i]
        self.blanks=[]
        def coH():
            for k,v in hblanks.items():
                if(k in self.blanks):
                    continue
                else:
                    self.blanks.append(k)
                    yield 0
            yield 0
        def coV():
            for k,v in vblanks.items():
                if(k in self.blanks):
                    continue
                else:
                    self.blanks.append(k)
                    yield True
            yield False
        a=coH()
        b=coV()
        for i in range(len(hblanks)):
            next(a)
            next(b)
            if(len(self.blanks)==len(hblanks)):
                break

        self.slotLen={}
        for k,v in self.hSlotLut.items():
            self.slotLen[k]=(self.slots[self.hSlotLut[k]].size,self.slots[self.vSlotLut[k]].size)

        self.slots={}
        i1=i2=0
        while True:
            if(i1>=len(self.hslots) and i2>=len(self.vslots)):
                break
            if(i1>=len(self.hslots)):
                if(i2<len(self.vslots)):
                    self.slots[self.vslotsKeys[i2]]=self.vslots[self.vslotsKeys[i2]]
                    i2+=1
            elif(i2>=len(self.vslots)):
                if(i1<len(self.hslots)):
                    self.slots[self.hslotsKeys[i1]]=self.hslots[self.hslotsKeys[i1]]
                    i1+=1
            else:
                self.slots[self.hslotsKeys[i1]]=self.hslots[self.hslotsKeys[i1]]
                i1+=1
                self.slots[self.vslotsKeys[i2]]=self.vslots[self.vslotsKeys[i2]]
                i2+=1

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
        for k,v in self.wordsbylen.items():
            weightDict={}
            for w in v:
                weight=0
                for i in w:
                    weight+=self.letterWeight[i]
                weightDict[w]=weight
            sortedWords=[k for k,v in sorted(weightDict.items(),key=lambda x:x[1],reverse=True)]
            # sortedWords=[k for k,v in weightDict.items()]
            self.wordsbylen[k]=sortedWords
        self.slotDict={}
        for k,v in self.slots.items():
            self.slotDict[k]=[]
            pattern=self.slot2str(v)
            if(not pattern.strip()):
                self.slotDict[k]=copy.deepcopy(self.wordsbylen[v.size])
            for w in self.wordsbylen[v.size]:
                flag=True
                for i in range(len(w)):
                    if(pattern[i]==' ' or pattern[i]==w[i]):
                        continue
                    else:
                        flag=False
                        break
                if(flag):
                    self.slotDict[k].append(w)
    
    def loadWords(self,filename):
        if(not hasattr(self,'trieDict')):
            self.trieDict={}
        words=[]
        freq={}
        validLengths=set([v.size for k,v in self.slots.items()])
        with open(filename,'r') as f:
            for w in f:
                w=w.strip()
                if(len(w) in validLengths):
                    words.append(w)
                for i in w.strip():
                    if(i not in freq):
                        freq[i]=1
                    else:
                        freq[i]+=1
        self.words=np.array(words)
        self.freq={k: v//100 for k, v in sorted(freq.items(),key=lambda x:x[1],reverse=True)}
        for k,v in self.freq.items():
            if(k in ['A','E','I','O','U']):
                self.freq[k]*=3
        self.freq={k:v for k,v in sorted(self.freq.items(),key=lambda x:x[1],reverse=True)}
        self.letterWeight={}
        for k,v in freq.items():
            self.letterWeight[k]=v//100
        self.initWordsByLen()
        for length,wordList in self.wordsbylen.items():
            self.wordTrie[length]={}
            for i in range(len(wordList)):
                anchor=self.wordTrie[length]
                for j in range(len(wordList[i])):
                    if(wordList[i][j] not in anchor):
                        if(j==len(wordList[i])-1):
                            anchor[wordList[i][j]]=self.slot2str(wordList[i])
                        else:
                            anchor[wordList[i][j]]={}
                    anchor=anchor[wordList[i][j]]
        self.generateWordTries()

    def trieMatch(self,trieIdx,pattern,trie=None,isRoot=True):
        if(isRoot):
            try:
                return self.matchCache[pattern]
            except KeyError:
                try:
                    self.matchCache[pattern]=False
                except KeyError:
                    self.matchCache={}
                    self.matchCache[pattern]=False
            trie=self.slotTries[trieIdx]
            
        if(pattern and (not pattern.strip())):
            return True
        if(isinstance(trie,str)):
            if(not pattern):
                return True
            else:
                return False
        elif(pattern[0] in trie):
            result=self.trieMatch(trieIdx,pattern[1:],trie[pattern[0]],False)
            if(isRoot):
                self.matchCache[pattern]=result
            return result
        elif(pattern[0]==' '):
            result=False
            for k,v in trie.items():
                result|=self.trieMatch(trieIdx,pattern[1:],v,False)
                if(result):
                    break
            if(isRoot):
                self.matchCache[pattern]=result
            return result
        else:
            if(isRoot):
                self.matchCache[pattern]=False
            return False
                
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
            self.slotTries[k]=copy.deepcopy(self.wordTrie[len(slotstr)])
            self.sortTrieByWeight(self.slotTries,k)
            if(not slotstr.strip()):
                continue
            self.reduceTrie(self.slotTries,k,slotstr)
        
    def sortTrieByWeight(self,trie,idx):
        if(isinstance(trie[idx],str)):
            return
        trie[idx]={k:v for k,v in sorted(trie[idx].items(),key=lambda x:self.freq[x[0]],reverse=True)}
        for k,v in trie[idx].items():
            self.sortTrieByWeight(trie[idx],k)

        

    def word2trie(self,word,pos=0):
        if(len(word)==pos):
            return word
        return {word[pos]:self.word2trie(word,pos+1)}


    def getPreffix(self,h,v):
        hPre=''
        vPre=''
        if(v>0):
            for i in range(v-1,-1,-1):
                if(self.grid[h,i]=='*'):
                    break
                else:
                    hPre=self.grid[h,i]+hPre
        if(h>0):
            for i in range(h-1,-1,-1):
                if(self.grid[i,v]=='*'):
                    break
                else:
                    vPre=self.grid[i,v]+vPre
        return hPre,vPre
    
    def getLettersWithPreffix(self,trie,prefx):
        for i in range(len(prefx)):
            if(prefx[i] not in trie):
                return []
            else:
                trie=trie[prefx[i]]
        return list(trie.keys())

    def getIntersection(self,h,v):
        hp,vp=self.getPreffix(h,v)
        hlen,vlen=self.slotLen[h,v]
        try:
            return self.intersectionCache[hlen,vlen,hp,vp]
        except KeyError:
            pass
        hl=self.getLettersWithPreffix(self.slotTries[self.hSlotLut[h,v]],hp)
        vl=self.getLettersWithPreffix(self.slotTries[self.vSlotLut[h,v]],vp)
        res=[i for i in hl if i in vl]
        self.intersectionCache[hlen,vlen,hp,vp]=res
        return res
        
    def fitNextLetter(self,h,v,checkpoint=-1):
        letters=self.getIntersection(h,v)
        cur=checkpoint+1
        if(not letters or cur>=len(letters)):
            return False
        self.grid[h,v]=letters[cur]
        self.steptracks.append(((h,v),cur))
        return True
    
    def backtrack(self,h,v,checkpoint=-1):
        if(self.fitNextLetter(h,v,checkpoint)):
            try:
                nextH,nextV=self.blanks[self.blanks.index((h,v))+1]
            except IndexError:
                return True
            # nextTrie=self.slotTries[nextKey]
            return self.backtrack(nextH,nextV)
        return False

    def placeWords(self):
        if(not hasattr(self,'words') or len(self.words)==0):
            return False
        if(len(self.slotTries)<len(self.slots)):
            return False
        # print(self.getPreffix(2,5))
        self.debug=0
        self.hit=0
        self.cacheSearch=0
        self.steptracks=[]  # e=(pos:tuple; checkpoint:int)
        if(self.isSolved()):
            return True
        h,v=self.blanks[0]
        checkpoint=-1
        while(not self.backtrack(h,v,checkpoint)):
            if(not len(self.steptracks)):
                return False
            lastStep=self.steptracks[-1]
            h,v=lastStep[0]
            # slotIdx=lastStep[0]
            checkpoint=lastStep[1]
            self.grid[h,v]=' '
            del self.steptracks[-1]
        # print(self.grid)
        return True

    def fill_with_given_words(self,wordsfile,texfile):
        self.loadWords(wordsfile)
        self.initWordsByLen()
        texname=texfile if texfile.startswith('filled_') else 'filled_'+texfile
        if(self.placeWords()):
            self.saveToTex(texname)
            print(f"I filled it!\nResult captured in {texname}.")
        else:
            print("Hey, it can't be filled with these words!")

    def saveToTex(self,texfile):
        f=open(texfile,'w')
        f.write('\\documentclass{standalone}\n\\usepackage{pas-crosswords}\n\\usepackage{tikz}\n\n\\begin{document}\n\\begin{tikzpicture}\n')
        for i in range(self.height):
            if(i==0):
                f.write('\\gridcross{'+self.slot2str(self.grid[i]))
            else:
                f.write(' '*11+self.slot2str(self.grid[i]))
            if(i!=self.height-1):
                f.write(',')
            f.write('%\n')
        f.write(' '*10+'}\n')
        f.write('\\end{tikzpicture}\n\\end{document}\n')
        
    def solve(self,texfile,dictfile='dictionary.txt'):
        start_time = time.time()
        self.loadWords(dictfile)
        self.initWordsByLen()
        texname=texfile if texfile.startswith('solved_') else 'solved_'+texfile
        if(self.placeWords()):
            self.saveToTex(texname)
            print(f"I solved it!\nResult captured in {texname}.")
        else:
            print("Hey, it can't be solved!")
        # print(self.grid)
        end_time = time.time()
        print(end_time-start_time,'secs')
        # print(self.debug)
        # print(f'{self.hit/(self.nohit+self.hit)*100}%')
        return


if __name__=='__main__':
    a=Crossword('ass2/empty_grid_3.tex')
    print(a)
    a.solve('test.tex',dictfile='ass2/dictionary.txt')



