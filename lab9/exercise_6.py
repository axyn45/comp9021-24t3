# You can assume that word_pairs() is called with a string of
# uppercase letters as agument.
#
# dictionary.txt is stored in the working directory.
#
# Outputs all pairs of distinct words in the dictionary file, if any,
# that are made up of all letters in available_letters
# (if a letter in available_letters has n occurrences,
# then there are n occurrences of that letter in the combination
# of both words that make up an output pair).
#
# The second word in a pair comes lexicographically after the first word.
# The first words in the pairs are output in lexicographic order
# and for a given first word, the second words are output in
# lexicographic order.
#
# Hint: If you do not know the imported Counter class,
#       experiment with it, passing a string as argument, and try
#       arithmetic and comparison operators on Counter objects.


from collections import Counter
dictionary_file = 'dictionary.txt'


def word_pairs(available_letters):
    '''
    >>> word_pairs('ABCDEFGHIJK')
    >>> word_pairs('ABCDEF')
    CAB FED
    >>> word_pairs('ABCABC')
    >>> word_pairs('EOZNZOE')
    OOZE ZEN
    ZOE ZONE
    >>> word_pairs('AIRANPDLER')
    ADRENAL RIP
    ANDRE APRIL
    APRIL ARDEN
    ARID PLANER
    ARLEN RAPID
    DANIEL PARR
    DAR PLAINER
    DARER PLAIN
    DARNER PAIL
    DARPA LINER
    DENIAL PARR
    DIRE PLANAR
    DRAIN PALER
    DRAIN PEARL
    DRAINER LAP
    DRAINER PAL
    DRAPER LAIN
    DRAPER NAIL
    ERRAND PAIL
    IRELAND PAR
    IRELAND RAP
    LAIR PANDER
    LAND RAPIER
    LAND REPAIR
    LANDER PAIR
    LARDER PAIN
    LEARN RAPID
    LIAR PANDER
    LINDA RAPER
    NADIR PALER
    NADIR PEARL
    NAILED PARR
    PANDER RAIL
    PLAN RAIDER
    PLANAR REID
    PLANAR RIDE
    PLANER RAID
    RAPID RENAL
    '''
    words=[]
    wordsByLen={}
    wordsTrie={}
    with open(dictionary_file,'r') as f:
        for i in f:
            i=i.strip()
            words.append(i)
            try:
                wordsByLen[len(i)].append(i)
            except KeyError:
                wordsByLen[len(i)]=[i]
    wordsByLen={k:v for k,v in sorted(wordsByLen.items(),key=lambda x:x[0])}
    def helper(trie,key,word,idx):
        if(idx==len(word)):
            trie[key]=word
            return
        if(word[idx] not in trie[key]):
            trie[key][word[idx]]={}
        helper(trie[key],word[idx],word,idx+1)
    for l,words in wordsByLen.items():
        wordsTrie[l]={}
        for word in words:
            helper(wordsTrie,l,word,0)
    def match(p1,p2):
        p2=list(p2)
        for i in p1:
            if(i not in p2):
                return False
            p2.remove(i)
        return True
    def removeFrom(s1,s2):
        cp=list(s2)
        for i in s1:
            cp.remove(i)
        return ''.join(cp)
    def getSortedTuple(e1,e2):
        if(e1<=e2):
            return (e1,e2)
        else:
            return (e2,e1)
    def tupleToStr(tup):
        return tup[0]+' '+tup[1]
            
    available_letters=list(available_letters)
    available_letters.sort(key=lambda x:ord(x))
    res=[]
    span=(len(available_letters)-5)//2+(1 if (len(available_letters)-5)%2 else 0)
    for i in range(3,3+span):
        if(not i in wordsByLen or not len(available_letters)-i in wordsByLen):
            continue
        words1=wordsByLen[i]
        for j in words1:
            if(match(j,available_letters)):
                newletters=removeFrom(j,available_letters)
                words2=wordsByLen[len(available_letters)-i]
                for k in words2:
                    if(match(k,newletters) and j!=k):
                        output=tupleToStr(getSortedTuple(j,k))
                        if(output not in res):
                            res.append(output)
    res.sort()
    for i in res:
        print(i)
    pass
    # REPLACE PASS ABOVE WITH YOUR CODE
                

if __name__ == '__main__':
    # word_pairs('AIRANPDLER')
    import doctest
    doctest.testmod()
