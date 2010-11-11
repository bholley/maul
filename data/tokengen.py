import os, sys, re
sys.path.append('../src/')
from uaobj import *


def main():
    tokendict = {}
    ualist = readFile('uadata_CLEAN.txt')
    print "Number of UA Strings: ", len(ualist)
    for (i,x) in enumerate(ualist):
        tokenlist = gentokenlist(x)
        for tok in tokenlist:
            try:
                tokendict[tok]
            except KeyError:
                tokendict[tok] = 1
            else:
                tokendict[tok] = tokendict[tok] + 1
    f = open('tokens.txt','w')			
    keysort = dsort(tokendict)
    for k in keysort:
        s = "'"+k+"' "+str(tokendict[k])
        f.write(s+'\n')

    return 0


def gentokenlist(x):
    k = 3
    uaString = x.uaString	
    tokenlist = []
    for index in range(len(uaString)-k+1):	
        tokenlist.append(uaString[index:index+3])
    return tokenlist	
		

def dsort(dic): # return sorted list of keys
    items = [(v,k) for k,v in dic.items()]
    items.sort(reverse=True)
    return [k for (v,k) in items]

if __name__ == "__main__":
    main()

