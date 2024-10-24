# EDIT THE FILE WITH YOUR SOLUTION
import re
import numpy as np

class Crossword:
    def __init__(self,filename) -> None:
        # print(filename)
        self.rawtex=[]
        self.tex=''
        self.blackcases=[]
        self.vwords=[]
        self.hwords=[]
        self.letterscount=0

        with open('ass2/dictionary.txt','r') as d:
            self.dictionary=np.array(list(d))

        with open(filename,'r') as f:
            for l in f:
                self.rawtex.append(l)
                self.tex+=l.split('%')[0].replace(' ','').strip()

        matches=re.findall(r'(?<=\\begin{crossgrid}\[)[hv=,\d]*(?=])',self.tex)
        if(len(matches)):
            matches=matches[0].split(',')
            self.width=int(matches[0].split('=')[1])
            self.height=int(matches[1].split('=')[1])

        matches=re.findall(r'(?<=\\blackcases{)[\d\/,]*(?=})',self.tex)
        if(len(matches)):
            matches=matches[0].split(',')
            for i in matches:
                coord=i.split('/')
                self.blackcases.append((int(coord[1])-1,int(coord[0])-1))
        
        matches=re.findall(r'(?<=\\words\[v\]{)[\d\/,a-zA-Z]*(?=})',self.tex)
        if(len(matches)):
            matches=matches[0].split(',')
            for i in matches:
                coord=i.split('/')
                self.vwords.append((int(coord[1])-1,int(coord[0])-1,coord[2]))

        matches=re.findall(r'(?<=\\words\[h\]{)[\d\/,a-zA-Z]*(?=})',self.tex)
        if(len(matches)):
            matches=matches[0].split(',')
            for i in matches:
                coord=i.split('/')
                self.hwords.append((int(coord[1])-1,int(coord[0])-1,coord[2]))

        for i in self.vwords+self.hwords:
            self.letterscount+=len(i[2])

        self.grid=np.array([['' for _ in range(self.width)] for _ in range(self.height)])
        
        for i in self.blackcases:
            self.grid[i[0],i[1]]='*'
        for i in self.vwords:
            self.grid[i[0]:i[0]+len(i[2]),i[1]]=list(i[2])
        for i in self.hwords:
            self.grid[i[0],i[1]:i[1]+len(i[2])]=list(i[2])
    
    def __str__(self):
        ctV=0
        ctH=0
        for i in self.grid.T:
            notcomplete=False
            for j in range(len(i)):
                if(i[j]=='' or ('*'==i[j] and (j==0 or i[j-1]==i[j]))):
                    notcomplete=True
                if(i[j]=='*' or j==len(i)-1):
                    if(not notcomplete):
                        ctV+=1
                    notcomplete=False
        for i in self.grid:
            notcomplete=False
            for j in range(len(i)):
                if(i[j]=='' or ('*'==i[j] and (j==0 or i[j-1]==i[j]))):
                    notcomplete=True
                if(i[j]=='*' or j==len(i)-1):
                    if(not notcomplete):
                        ctH+=1
                    notcomplete=False
        return (f'A grid of width {self.width} and height {self.height}, with {len(self.blackcases) if len(self.blackcases) else "no"} blackcase{"" if len(self.blackcases)==1 else "s"}, filled with {self.letterscount if self.letterscount else "no"} letter{"" if self.letterscount==1 else "s"},\nwith {ctV if ctV else "no"} complete vertical word{"" if ctV==1 else "s"} and {ctH if ctH else "no"} complete horizontal word{"" if ctH==1 else "s"}.')
        
    # def countCompleted(self):
    #     ctV=0
    #     ctH=0
    #     for i in self.grid.T:
    #         notcomplete=False
    #         for j in range(len(i)):
    #             if(i[j]=='' or ('*'==i[j] and (j==0 or i[j-1]==i[j]))):
    #                 notcomplete=True
    #             if(i[j]=='*' or j==len(i)-1):
    #                 if(not notcomplete):
    #                     ctV+=1
    #                 notcomplete=False
    #     for i in self.grid:
    #         notcomplete=False
    #         for j in range(len(i)):
    #             if(i[j]=='' or ('*'==i[j] and (j==0 or i[j-1]==i[j]))):
    #                 notcomplete=True
    #             if(i[j]=='*' or j==len(i)-1):
    #                 if(not notcomplete):
    #                     ctH+=1
    #                 notcomplete=False
    #     return ctV,ctH




if __name__=='__main__':
    a=Crossword('ass2/partial_grid_1.tex')
    print(a)
    print(a.countCompleted())