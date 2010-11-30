import sys,re,os
from StringSVM import StringSVM
from SVMParams import SVMParams
from DecisionProblem import DecisionProblem
import sqlite3
import random
from AgentTypeTokenCLI import runSVM

def runCV():

# set up lists of CV params
# this is a subsequence CV so we have to CV:
# C
# seqLen
# seqLambda
# good values for C can range on a log scale, so lets run
# for now 0.1 1 10 100 1000
# for seqLen lets run 4 5 6 7 8 9 10
# for Lambda, lets do  a coarse search
#    Clist = [0.1, 1.0, 10.0, 100.0, 1000.0] finished 0.1 already
#    Clist = [5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    Clist = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    LenList = [5] 
    LambdaList = [0.9]
#    Clist = [1.0]
#    LenList = [5]
#    LambdaList = [0.9]

# 10 is looking best right now

    f = open('models/Type/CVoutput.txt','a') 
    for C in Clist:
        for seqLen in LenList:
            for seqLambda in LambdaList:
                print C,seqLen,seqLambda
                accuracy,correct0,false0,correct1,false1 = runSVM(float(C),int(seqLen),float(seqLambda))
                s = str(C)+" " + str(seqLen) + " " + str(seqLambda) + " "
                s = s + str(accuracy) + " " + str(correct0) + " " + str(false0) + " "
                s = s + str(correct1) + " " + str(false1)
                f.write(s+'\n')

    f.close()
    return

if __name__ == "__main__":
    runCV()


