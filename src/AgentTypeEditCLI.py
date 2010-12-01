import sys, os, re
from StringSVM import StringSVM
from SVMParams import SVMParams
from DecisionProblem import DecisionProblem
import sqlite3
import random


def runSVMedit(C,gamma):

#initialize with seed so we get same training and test sets every time
# i.e. for cross validation
    random.seed(18283835) # use this for standard validation
#    random.seed(8982101)
#    random.seed(12820501)

# Throwaway test to classify browser vs bot
    frac = 0.8

# Open the database
    conn = sqlite3.connect("mydb")
    conn.text_factory = str
    c = conn.cursor()

# Data
    trainingData = [];
    testData = [];

    trainlist = []
    testlist = []
# bots
    c.execute('select uaString from data where "Type" = "Robot"')
    uaslist = []
    for uaString in c:
        uaslist.append(uaString[0])
    nrobot = len(uaslist)
    random.shuffle(uaslist)
    for uaString in uaslist[0:int(round(frac*nrobot,0))]:
        trainingData.append(('Robot', uaString))
        trainlist.append(uaString)
    for uaString in uaslist[int(round(frac*nrobot,0)):len(uaslist)+1]:
        testData.append(('Robot', uaString))
        testlist.append(uaString)
    print 'Number robots selected for training: ', int(round(frac*nrobot,0))

# browsers
    c.execute('select uaString from data where "Type" = "Browser"')
    uaslist = []
    for uaString in c:
        uaslist.append(uaString[0])
    nbrowser = len(uaslist)
    random.shuffle(uaslist)
    for uaString in uaslist[0:int(round(frac*nbrowser,0))]:
        trainingData.append(('Browser', uaString))
        trainlist.append(uaString)
    for uaString in uaslist[int(round(frac*nbrowser,0)):len(uaslist)+1]:
        testData.append(('Browser', uaString))
        testlist.append(uaString)
    print 'Number browsers selected for training: ', int(round(frac*nbrowser,0))    
    
# just select first 5000 elements of train data and first 1000 elements of test data
#    random.shuffle(trainingData)    
#    random.shuffle(testData)
#    trainingData = trainingData[0:1000]
#    testData = testData[0:200]


# Make a Decision Problem
    params = SVMParams()
    params.kernelName = "edit"
    params.tokenized = False
    params.C = C
    params.gamma = gamma
    decProb = DecisionProblem("Type", params)

# If the model is not already generated, generate it
    if not decProb.haveModel():
        decProb.generateModel(trainingData)
        decProb.saveModel()
    else:
        decProb.loadModel()

# Predict
    correct = 0.0
    total = 0.0
    correct0 = 0.0
    correct1 = 0.0
    false1 = 0.0
    false0 = 0.0
    ind = 0
    fmiss = open('misclass.txt','w')
    for actual, ua in testData:
        prediction = decProb.decide(ua)
        if( actual == 'Robot'):
            if(actual == prediction):
                correct0 = correct0 + 1.0
                correct = correct + 1.0
            else:
                false1 = false1 + 1.0
                fmiss.write('false Browser: ' + testlist[ind]+'\n')
        elif( actual == 'Browser'):
            if(actual == prediction):
                correct1 = correct1 + 1.0
                correct = correct+1.0
            else:
                false0 = false0 + 1.0
                fmiss.write('false Robot: ' + testlist[ind] +'\n')
    
        total = total + 1.0
        ind = ind + 1

    print "ACCURACY: ", correct / total
    print "False X means classifier said data was X, but it was actually something else"
    print "Correct Robot: ", correct0, "False Robot: ", false0
    print "Correct Browser: ", correct1, "False Browser: ", false1

    fname = decProb.modelPath() + ".results"
    f = open(fname,'w')
    f.write(str(decProb.svm.labelMap)+'\n')
    s = "ACCURACY: " + str(correct/total) + '\n'
    s = s + "False X means classifier said data was X, but it was actually something else\n"
    s = s + "Correct 0: " + str(correct0) + " False 0: " + str(false0) + '\n'
    s = s + "Correct 1: " + str(correct1) + " False 1: " + str(false1) + '\n'
    f.write(s)
    accuracy = correct/total    
    return accuracy,correct0,false0,correct1,false1

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print "You need to specify C, gamma in that order space delimited"
        sys.exit(2)
    C = float(sys.argv[1])
    gamma = float(sys.argv[2])
    runSVMedit(C,gamma)
