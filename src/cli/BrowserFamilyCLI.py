import sys, os, re
from StringSVM import StringSVM
from SVMParams import SVMParams
from DecisionProblem import DecisionProblem
import sqlite3
import random


def runSVM(C,gamma):

#initialize with seed so we get same training and test sets every time
# i.e. for cross validation
    random.seed(18283835)

# Throwaway test to classify browser vs bot
    frac = 0.8

# Open the database
    conn = sqlite3.connect("mydb")
    conn.text_factory = str
    c = conn.cursor()

# Data
    trainingData = [];
    testData = [];

#get Families
    c.execute('select Tokens, Family from data where "Type" = "Browser" AND "Family" IS NOT NULL')
    uaslist = []
    familylist = []
    for row in c:
        uaslist.append([row[0],row[1]]) # stored as list of lists
    nbrowser = len(uaslist)
    random.shuffle(uaslist)
    for uaString in uaslist[0:int(round(frac*nbrowser,0))]:
        tokens = [int(s) for s in uaString[0].split(" ")]
        family = uaString[1] 
        trainingData.append((family, tokens))
    for uaString in uaslist[int(round(frac*nbrowser,0)):len(uaslist)+1]:
        tokens = [int(s) for s in uaString[0].split(" ")]
        family = uaString[1]
        testData.append((family, tokens))
    print 'Number browsers selected for training: ', int(round(frac*nbrowser,0))    
    
# just select first 5000 elements of train data and first 1000 elements of test data
#    random.shuffle(trainingData)    
#    random.shuffle(testData)
#    trainingData = trainingData[0:1000]
#    testData = testData[0:200]


# Make a Decision Problem
    params = SVMParams()
    params.kernelName = "edit"
    params.tokenized = True
    params.C = C
    params.gamma = gamma
    decProb = DecisionProblem("Family", params)

# If the model is not already generated, generate it
    if not decProb.haveModel():
        decProb.generateModel(trainingData)
        decProb.saveModel()
    else:
        decProb.loadModel()

# Predict
# FIXME need to build in confusion matrix for these multiclass problems
    correct = 0.0
    total = 0.0
    for actual, ua in testData:
        prediction = decProb.decide(ua)
        if(actual == prediction):
            correct = correct + 1.0
        total = total + 1.0

    print "ACCURACY: ", correct / total

    fname = decProb.modelPath() + ".results"
    f = open(fname,'w')
    f.write(str(decProb.svm.labelMap)+'\n')
    s = "ACCURACY: " + str(correct/total) + '\n'
    f.write(s)
    accuracy = correct/total    
    return accuracy

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print "You need to specify C, gamma in that order space delimited"
        sys.exit(2)
    C = float(sys.argv[1])
    gamma = float(sys.argv[2])
    runSVM(C,gamma)
