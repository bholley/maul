import sys,re,os
from StringSVM import StringSVM
from SVMParams import SVMParams
from DecisionProblem import DecisionProblem
import sqlite3
import random
from AgentTypeTokenEditCLI import runSVMedittoken

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
    Clist = [0.6, 0.8, 1.0 ]
    gammalist = [0.01, 0.05, 0.1] 

# 10 is looking best right now

    f = open('models/Type/CVoutputedittoken.txt','a') 
    for C in Clist:
        for gamma in gammalist:
                print C,gamma
                accuracy,correct0,false0,correct1,false1 = runSVMedittoken(float(C),float(gamma))
                s = str(C)+" " +  str(gamma) + " "
                s = s + str(accuracy) + " " + str(correct0) + " " + str(false0) + " "
                s = s + str(correct1) + " " + str(false1)
                f.write(s+'\n')

    f.close()
    return

if __name__ == "__main__":
    runCV()


