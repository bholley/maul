import sys,os,re
sys.path.append('../src/')
from uaobj import *
import math
from tokengen import dsort
from Common import *



def tokenscore(prop,value,fname):
    print "Tokenscoring.py called with prop: " + prop + " and value: " + value
    
    ualist = readFile(fname)
    tokens = dict()
    for x in ualist:
        toklist = [int(y) for y in x.data['Tokens'].split(' ')]
        for t in toklist:
            try:
                tokens[t]
            except KeyError:
                tokens[t] = 1
            else:
                tokens[t] = tokens[t] + 1
    # now compute mutual information score for each token
    scoredict = dict()
#    cnt = 0
    for k,v in tokens.items():
        print k
        scoredict[k] = score(k,prop,value,ualist)
        print scoredict[k]
#        cnt = cnt + 1
#        if cnt > 10:
#            break
        
# need to remove ua's without the proper type first, before calling this function which is dumb
#    I = score(0,'Type','Browser',ualist)
#    print I
    keylist = dsort(scoredict)        
    fout = 'tokenscores_'+value+'.txt'
    f = open(fout,'w')
    for k in keylist:
        s = str(k) + ': ' +str(scoredict[k])+'\n'
        f.write(s)
    f.close()    

def score(token,prop,value,ualist):
# format is first number is token, second number is property value
# i.e. X is token, Y is property value
    p11 = 0.0
    p00 = 0.0
    p01 = 0.0
    p10 = 0.0
    p1 = [0,0]
    p2 = [0,0]
    p = [p1,p2]
    token = int(token)
# clean ualist so that the prop exists
    totcnt = 0.0 
    valcnt = 0.0
    for x in ualist:
        toktup = [int(y) for y in tuple(x.data['Tokens'].split(' '))]
        try:
            x.data[prop]
        except KeyError:
            # do nothing
            continue
        else:
            totcnt = totcnt + 1.0
            # try this code p[token in toktup][x.data[prop]==value]+=1
            if(x.data[prop] == value):
                valcnt = valcnt+1.0
                if token in toktup:
                    p[1][1] = p[1][1] + 1.0
                elif token not in toktup:
                    p[0][1] = p[0][1] + 1.0
            else:
                if token in toktup:
                    p[1][0] = p[1][0] + 1.0
                elif token not in toktup:
                    p[0][0] = p[0][0] + 1.0

    p[1][1] = p[1][1]/totcnt
    p[0][0] = p[0][0]/totcnt
    p[0][1] = p[0][1]/totcnt
    p[1][0] = p[1][0]/totcnt
    pX = [0,0]
    pY = [0,0]
    for a in (0,1):
        for b in (0,1):
            pX[a] = pX[a] + p[a][b]
            pY[a] = pY[a] + p[b][a]
    I = 0.0
    for a in (0,1):
        for b in (0,1):
           if p[a][b] == 0.0:
               I = I + 0.0
           else:
               I = I + p[a][b]*math.log(p[a][b]/(pX[a]*pY[b]),2)

#    print p[1][1],p[0][0],p[0][1],p[1][0],pX,pY
#    print valcnt
#    print totcnt

    return I

def PrintUsage():
    print "Usage: " + sys.argv[0] + " <Property> <Value> <filename>"
    print "Example: " + sys.argv[0] + " Type Browser uadata_clean_token.txt"


if __name__ == "__main__":
    if len(sys.argv) < 4:
        PrintUsage()
        sys.exit(2)
    prop = sys.argv[1]
    value = sys.argv[2]
    fname = sys.argv[3]
    if prop not in categories:
        raise RuntimeError("Unknown Property")
    tokenscore(prop,value,fname)
