# EDIT THE FILE WITH YOUR SOLUTION
import re
import numpy as np

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
        self.sortedHSlots=[]
        self.sortedVSlots=[]
        self.sortedSlots=[]

        for i in range(self.height):
            startpos=0
            for j in range(self.grid[i].size+1):
                if(j==self.grid[i].size or self.grid[i,j]=='*'):
                    if(not startpos==j and j-startpos>1):
                        self.hSlots.append(self.grid[i,startpos:j])
                    startpos=j+1
        for i in range(self.width):
            startpos=0
            for j in range(self.grid.T[i].size+1):
                if(j==self.grid.T[i].size or self.grid.T[i,j]=='*'):
                    if(not startpos==j and j-startpos>1):
                        self.vSlots.append(self.grid.T[i,startpos:j])
                    startpos=j+1

        self.sortedHSlots=sorted(self.hSlots,key=lambda x:x.size)
        self.sortedVSlots=sorted(self.vSlots,key=lambda x:x.size)
        self.sortedSlots=sorted(self.sortedHSlots+self.sortedVSlots,key=lambda x:x.size)
        # pass

    def clearGrid(self):
        for i in range(self.height):
            for j in range(self.width):
                if(not (self.grid[i,j]==' ' or self.grid[i,j]=='*')):
                    self.grid[i,j]=' '
                    
    def initWordsByLen(self):
        if(not hasattr(self,'wordsbylen')):
            self.wordsbylen={}
        validLengths=set([i.size for i in self.hSlots]+[i.size for i in self.vSlots])
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
        validLengths=set([i.size for i in self.hSlots]+[i.size for i in self.vSlots])
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
        self.generateWordTries4Slots()
        # try:
        #     print(self.trieDict[3]['A']['X']['N'])
        # except KeyError:
        #     print('no such word')
        # pass


    # def validatePattern(pattern):
    def validate(self):
        
        for slot in self.sortedSlots:
            pattern=self.slot2str(slot)
            # for i in slot:
                # if(i==' '):
                #     pattern+=r'\w'
                # else:
                # pattern+=i
            # matches=re.match(pattern,self.wordslongbylen[slot.size])
            anchor=self.trieDict[len(pattern)]
            try:
                for i in range(len(pattern)):
                    if(pattern[i]==' '):
                        True
                    anchor=anchor[pattern[i]]
            except KeyError:
                return False
            # if(not matches):
            #     return False
        return True
                

    def isSolved(self):
        for i in self.sortedSlots:
            if(np.isin(' ',i)):
                return False
        return True

    def slot2str(self,slot):
        result=''
        for i in slot:
            result+=i
        return result
    
    def generateWordTries4Slots(self):
        def helper(anchor,pattern,debug):
            if(isinstance(anchor,str) and not pattern):
                return True
            result=False
            for k,v in anchor.copy().items():
                if(k!=pattern[0] and not pattern[0]==' '):
                    del anchor[k]
                    pass
                # elif(not helper(v,pattern[1:] if len(pattern)>1 else '',debug+k)):
                else:
                    result|=helper(v,pattern[1:] if len(pattern)>1 else '',debug+k)
            return result
            # if(not helper(v,pattern[1:] if len(pattern)>1 else '',debug+k))
            # for k,v in anchor.copy().items():
            #     if(pattern[0]!=k and pattern[0]!=' '):
            #         del anchor[k]
            #         # return False
            #     else:
            #         result|=helper(v,pattern[1:] if len(pattern)>1 else '',debug+k)
            # return result
                

        if(not hasattr(self,'possibleTries')):
            self.possibleTries={}
        for i in range(len(self.hSlots)):
            slotstr=self.slot2str(self.hSlots[i])
            if(' ' not in slotstr):
                self.possibleTries[('h',i)]=slotstr
                continue
            self.possibleTries[('h',i)]=self.trieDict[len(slotstr)]
            if(not slotstr.strip()):
                continue
            # pattern=self.slot2str(self.hSlots[i])
            helper(self.possibleTries[('h',i)],slotstr,'')
        pass


    
    def fitNextWord(self,slotIdx,prevWord):
        # if(not self.steptracks):
        #     slotIdx=0
        #     prevWord=None
        # else:
        #     slotIdx=len(self.steptracks)
        #     prevWord=self.steptracks[-1][]
        wordList=self.wordsbylen[self.sortedSlots[slotIdx].size]
        # wordLong=self.wordslongbylen[self.sortedSlots[slotIdx].size]
        if(not prevWord):
            prevWordIdx=-1
        else:
            prevWordIdx=wordList.index(prevWord)
        if(prevWordIdx==len(wordList)-1):
            return False
        # pattern=''
        # for i in self.sortedSlots[slotIdx]:
        #     if(i==' '):
        #         pattern+='\w'
        #     else:
        #         pattern+=i
        pattern=self.slot2str(self.sortedSlots[slotIdx]).replace(' ',r'\w')
        for i in range(prevWordIdx+1,len(wordList)):
            self.debug+=1
            if(self.debug%2000==0):print(self.debug,slotIdx,i,pattern)
            matches=re.match(pattern,wordLong)
            if(matches):
                temp=pattern.replace(r'\w',' ')
                self.sortedSlots[slotIdx][:]=list(wordList[i])
                if(not self.validate()):
                    self.sortedSlots[slotIdx][:]=list(temp)
                    continue
                self.steptracks.append((slotIdx,pattern.replace(r'\w',' '),wordList[i]))
                # self.sortedSlots[slotIdx][:]=list(wordList[i])
                return True
        return False

    
    def backtrack(self,idx,prevWord):
        if(idx==len(self.sortedSlots)):
            return True
        # if(not self.steptracks):
        #     if(len(self.wordsbylen[self.sortedSlots[0].size])==0):
        #         return False
        #     if(not self.fitNextWord()):
        #         if(not len(self.steptracks)):
        #             return False
        #         self.sortedSlots[self.steptracks[-1]]
        if(self.fitNextWord(idx,prevWord)):
            return self.backtrack(idx+1,'')
        return False
        

    def placeWords(self):
        if(not hasattr(self,'steptracks')):
            self.steptracks=[]  # e=(pos:int; prevstate:string; newstate:string)
        if(self.isSolved()):
            return True
        slotIdx=0
        prevWord=''
        while(not self.backtrack(slotIdx,prevWord)):
            if(not len(self.steptracks)):
                return False
            lastStep=self.steptracks[-1]
            self.sortedSlots[lastStep[0]][:]=list(lastStep[1])
            del self.steptracks[-1]
            prevWord=lastStep[2].strip()
            slotIdx=lastStep[0]

            # slotIdx=self.steptracks[-1][0]
            # prevWord=self.steptracks[-1][1]
            # self.sortedSlots[self.steptracks[-1][0]][:]=list(prevWord)
            # del self.steptracks[-1]
            # prevWord=prevWord.strip()
        return True



                    

    def fill_with_given_words(self,wordsfile,texfile):
        # self.splitSlots()
        self.loadWords(wordsfile)
        self.initWordsByLen()
        if(self.placeWords()):
            print(f"I filled it!\nResult captured in filled_{texfile}")
        else:
            print("Hey, it can't be filled with these words!")
        return

    def solve(self,texfile,dictfile='dictionary.txt'):
        self.loadWords(dictfile)
        self.initWordsByLen()
        if(self.placeWords()):
            print(f"I solved it!\nResult captured in solved_{texfile}")
        else:
            print("Hey, it can't be solved!")
        print(self.grid)
        return



if __name__=='__main__':
    a=Crossword('ass2/partial_grid_3.tex')
    print(a)
    a.solve('tete',dictfile='ass2/dictionary.txt')
    # a.fill_with_given_words('ass2/words_1.txt','test.tex')
    # print(a.splitArray)