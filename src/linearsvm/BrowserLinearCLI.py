import sys, os, re
from LinearSVMParams import *
from DecProblemStdKernels import *
from svmutil import *
import sqlite3
import random


def runSVM(C,seednum=18283835):

#initialize with seed so we get same training and test sets every time
# i.e. for cross validation
    if seednum == '-1':
        random.seed()
    else:
        random.seed(seednum)

# Throwaway test to classify browser vs bot
    frac = 0.8

# Open the database
    conn = sqlite3.connect("../mydb")
    conn.text_factory = str
    c = conn.cursor()

# Data
    trainingData = [];
    testData = [];

# read # of tokens
    ftokens = open('../../data/tokens.txt','r')
    keys = []
    for line in ftokens:
        s = line.strip().rstrip()
        token, sep, number = s.partition(' ')
        number = int(number) + 1
        keys.append(number)
    print 'NUMBER OF TOKENS: ', max(keys)
    maxtok = max(keys)
    print 'NUM TOKENS USED ', maxtok

#get Families
    c.execute('select Tokens, Family from data where "Type" = "Browser" AND "Family" IS NOT NULL')
#    c.execute('select Tokens, Family from data where "Type" = "Browser" AND ("Family" = "Firefox" OR "Family" = "IE" OR "Family" = "Chrome" OR "Family" = "Galeon" OR "Family" = "Konqueror" OR "Family" = "Opera" OR "Family" = "Safari" OR "Family" = "AOL Explorer" OR "FamilY" = "Maxthon" OR "Family" = "Avant Browser" OR "Family" = "IceWeasel" OR "Family" = "Mozilla" OR "Family" = "SeaMonkey" OR "Family" = "Netscape Navigator" OR "Family" = "Flock" OR "Family" = "Camino" OR "Family" = "Crazy Browser" OR "Family" = "CometBird" OR "Family" = "Epiphany" OR"Family" = "TheWorld Browser" OR "Family" = "K-Meleon" OR "Family" = "Sleipnir" OR "Family" = "Iron" OR "Family" = "Swiftfox" OR "Family" = "Acoo Browser" OR "Family" = "TT Explorer" OR "Family" = "GreenBrowser" OR "Family" = "Lunascape" OR "Family" = "OmniWeb" OR "Family" = "Other")')
    #c.execute('select Tokens, Family from data where "Type" = "Browser" AND ("Family" = "Firefox" OR "Family" = "IE")') # just firefox and IE, good debug test
#    c.execute('select Tokens, Family from data where "Type" = "Browser" AND ("Family" != "Other")')
    uaslist = []
    familylist = []
    for row in c:
        uaslist.append([row[0],row[1]]) # stored as list of lists
    nbrowser = len(uaslist)
    random.shuffle(uaslist)
    familydict = {}
    for uaString in uaslist[0:int(round(frac*nbrowser,0))]:
        tokens = [int(s)+1 for s in uaString[0].split(" ")]
        tokdict = {}
        for tok in tokens:
            if int(tok) < maxtok:
                try:
                    tokdict[int(tok)]
                except KeyError:
                    tokdict[int(tok)] = 1.0
                else:
                    tokdict[int(tok)] += 1.0
        family = uaString[1] 
        familydict[family] = 1
        trainingData.append((family, tokdict))
    for uaString in uaslist[int(round(frac*nbrowser,0)):len(uaslist)+1]:
        tokens = [int(s)+1 for s in uaString[0].split(" ")]
        tokdict = {}
        for tok in tokens:
            if int(tok) < maxtok:
                try:
                    tokdict[int(tok)]
                except KeyError:
                    tokdict[int(tok)] = 1.0
                else:
                    tokdict[int(tok)] += 1.0
        family = uaString[1]
        familydict[family] = 1
        testData.append((family, tokdict))
    print 'Number browsers selected for training: ', int(round(frac*nbrowser,0))    
    
# just select first 5000 elements of train data and first 1000 elements of test data
#    random.shuffle(trainingData)    
#    random.shuffle(testData)
#    trainingData = trainingData[0:1000]
#    testData = testData[0:200]
    print str(familydict)
    print len(familydict)

# Make a Decision Problem
    params = LinearSVMParams()
    params.kernelName = "linear"
    params.C = C
    decProb = DecisionProblem("Family", params)
    y, x = decProb.makedata(trainingData)
    options = decProb.genoptions()
    print options
    model = svm_train(y,x,options)

# If the model is not already generated, generate it
#    if not decProb.haveModel():
#        decProb.generateModel(trainingData)
#        decProb.saveModel()
#    else:
#        decProb.loadModel()

# Predict
# FIXME need to build in confusion matrix for these multiclass problems
    filename = decProb.modelPath()
    print 'Filename: ', filename
    print 'saving model'
    svm_save_model(filename,model)
    labelfile = filename+'.labels'
    flabel = open(labelfile,'w')
    for i,label in enumerate(set(decProb.labels)):
        s = label + ':'+str(i)+'\n'
        flabel.write(s)
    
    flabel.close()
    ytest, xtest = decProb.maketest(testData)
    pred_labels, (ACC,MSE,SCC), pred_values = svm_predict(ytest,xtest,model)

    correct = 0.0
    total = 0.0
    for i, actual in enumerate(ytest):
        #prediction = decProb.decide(ua)
        prediction = pred_labels[i]
        if(actual == prediction):
            correct = correct + 1.0
        else:
            print 'actual: ', actual, 'predicted: ',prediction
        total = total + 1.0

    print "ACCURACY: ", correct / total

    fname = decProb.modelPath() + ".results"
    f = open(fname,'w')
    f.write(str(decProb.labelMap)+'\n')
    s = "ACCURACY: " + str(correct/total) + '\n'
    f.write(s)
    accuracy = correct/total    
    return accuracy

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print "You need to specify C, gamma in that order space delimited"
        sys.exit(2)
    C = float(sys.argv[1])
    runSVM(C)
