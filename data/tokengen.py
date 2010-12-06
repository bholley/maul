import os, sys, re
sys.path.append('../src/')
from uaobj import *


def main():
    tokenfreq = {}
    tokendict = {}
    ualist = readFile('source/uadata_CLEAN.txt')
    print "Number of UA Strings: ", len(ualist)
    for (i,x) in enumerate(ualist):
        tokenlist = gentokenlist(x)
        for tok in tokenlist:
#            if tok == "(compatible;":
#                print tokenlist
#                print x
            try:
                tokenfreq[tok]
            except KeyError:
                tokenfreq[tok] = 1
            else:
                tokenfreq[tok] = tokenfreq[tok] + 1
    ffreq = open('tokens_frequency.txt','w')			
    ftok = open('tokens.txt','w')
    keysort = dsort(tokenfreq)
    for (i,k) in enumerate(keysort):
        s = k+" "+str(tokenfreq[k])
        ffreq.write(s+'\n')
        tokendict[k] = i
        s = k + ' ' + str(tokendict[k])
        ftok.write(s+'\n')
    ftok.close()
    ffreq.close()

# now generate a udata_clean_token.txt file
    fua = open('uadata_clean_token.txt','w')
    for x in ualist:
        uaString = x.uaString
        x.data['Tokens'] = ''
        for y in re.split('[.(),;/\s]',uaString):
            if not y == "":
                y = numcheck(y)
                x.data['Tokens'] = x.data['Tokens'] + str(tokendict[y]) + ' '
        fua.write(x+'\n')    
            


    return 0


def gentokenlist(x):
#    k = 3
    uaString = x.uaString	
    tokenlist = []
    for x in re.split('[.(),;/\s]',uaString):
        x = x.strip().rstrip()
        if not x == "":
            # number check            
            x = numcheck(x)
            tokenlist.append(x)

    return tokenlist
def numcheck(x): # check if is integer number
    # x is a string, check if it is a number
    x = x.strip().rstrip() # strip off any whitespace
    if x.isdigit():
        return str(len(x)) # return length of number
    else:
        return x # return just the string itself



# find all instances of parentheses strings
# find tokens in them without whitespace    
#    m = re.findall(r'\([^(]*(?:\([^(]*\))?[^(]*\)',uaString) # find any nested sets of paren 
#    for s in m:
#        s = s.strip().rstrip()
#        s = s.strip('(').rstrip(')') 
#        if ('(' in s) and (')' in s):
#            n = re.findall(r'\([^(]*\)',s)
#            for c in n:
#                c = c.strip().rstrip()
#                c = c.strip('(').rstrip(')')
#                if re.search(';',c): delim = ';'
#                elif re.search(',',c): delim = ','
#                else: delim = ';'    
#                for x in c.split(delim):
#                    x = x.strip().rstrip()
#                    if not x == "":
#                        if x == "(compatible;":
#                            print uaString + '\n' + 'c'
#                        tokenlist.append(x)
#            start = s.find('(')
#            end = s.find(')')
#            s = s.replace(s[start:end+1],'')
#        if re.search(';',s): delim = ';'
#        elif re.search(',',s): delim = ','
#        else: delim = ';'
#        for x in s.split(delim):
#            x = x.strip().rstrip()
#            if not x == "":
#                if x == "(compatible;":
#                    print uaString + '\n' + 's'
#                tokenlist.append(x)
# find strings outside of parentheses    
#    m = re.split(r'\([^(]*(?:\([^(]*\))?[^(]*\)',uaString)        
#    for s in m:
#        s = s.strip().rstrip()
#        s = s.strip('(').rstrip(')')
# assume delimited by spaces in these regions        
#    uacut = uaString            
#    for s in m:
#        uacut = uacut.replace(s,'')
#    for x in uacut.split(' '):
#        x = x.strip().rstrip()
#        if not x == "":
#            if x == "(compatible;":
#                print uaString + '\n' + 'n'
#            tokenlist.append(x)
#    for index in range(len(uaString)-k+1):	
#        tokenlist.append(uaString[index:index+3])
# look for tokens 

    return tokenlist	


def dsort(dic): # return sorted list of keys sorted by values
    items = [(v,k) for k,v in dic.items()]
    items.sort(reverse=True)
    return [k for (v,k) in items]

if __name__ == "__main__":
    main()
