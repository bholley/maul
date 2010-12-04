import sys, os, re
#from LinearSVM import *
from LinearSVMParams import *
from DecProblemStdKernels import *
from svmutil import *
import sqlite3
import random


def runSVMlinear(C=3.0,gamma=0.1,seednum= 18283835):

#initialize with seed so we get same training and test sets every time
# i.e. for cross validation
    if(seednum == '-1'):
        random.seed()
    else:    
        random.seed(seednum) # use this for standard validation
        #random.seed(8982101)
        #random.seed(12820501)

# Throwaway test to classify browser vs bot
    frac = 0.8

# Open the database
    conn = sqlite3.connect("../mydb")
    conn.text_factory = str
    c = conn.cursor()

# Data
    trainingData = [];
    testData = [];

    trainlist = []
    testlist = []

# read # of tokens 
    ftokens = open('../../data/tokens.txt','r')
    keys = []
    for line in ftokens:
        s = line.strip().rstrip()
        token, sep, number = s.partition(' ')
        number = int(number) + 1
        keys.append(number)
    print "NUMBER OF TOKENS: ",max(keys)    
    maxtok = max(keys)
    print "NUM TOKENS USED ", maxtok
# use first 500 tokens only
# bots
    c.execute('select Tokens, uaString from data where "Type" = "Robot"')
    uaslist = []
    for uaString in c:
        uaslist.append((uaString[0],uaString[1]))
    nrobot = len(uaslist)
    random.shuffle(uaslist)
    for Tok, uaString in uaslist[0:int(round(frac*nrobot,0))]:
        tokens = [int(s)+1 for s in Tok.split(" ")]
        tokdict = {}
  #      for key in keys: tokdict[int(key)] = 0
        for tok in tokens: 
            if int(tok) < maxtok:
                try:
                    tokdict[int(tok)]
                except KeyError:
                    tokdict[int(tok)] = 1.0
                else:
                    tokdict[int(tok)] +=1.0
        trainingData.append(('Robot', tokdict))
        trainlist.append(uaString)
    for Tok, uaString in uaslist[int(round(frac*nrobot,0)):len(uaslist)+1]:
        tokens = [int(s)+1 for s in Tok.split(" ")]
        tokdict = {}
  #      for key in keys: tokdict[int(key)] = 0
        for tok in tokens: 
            if int(tok) < maxtok:
                try:
                    tokdict[int(tok)]
                except KeyError:
                    tokdict[int(tok)] = 1.0
                else:
                    tokdict[int(tok)] +=1.0
        testData.append(('Robot', tokdict))
        testlist.append(uaString)
    print 'Number robots selected for training: ', int(round(frac*nrobot,0))

# browsers
    c.execute('select Tokens, uaString from data where "Type" = "Browser"')
    uaslist = []
    for uaString in c:
        uaslist.append((uaString[0],uaString[1]))
    nbrowser = len(uaslist)
    random.shuffle(uaslist)
    for Tok, uaString in uaslist[0:int(round(frac*nbrowser,0))]:
        tokens = [int(s)+1 for s in Tok.split(" ")]
        tokdict = {}
#        for key in keys: tokdict[int(key)] = 0
        for tok in tokens: 
            if int(tok) < maxtok:
                try:
                    tokdict[int(tok)]
                except KeyError:
                    tokdict[int(tok)] = 1.0
                else:
                    tokdict[int(tok)] +=1.0
        trainingData.append(('Browser', tokdict))
        trainlist.append(uaString)
    for Tok, uaString in uaslist[int(round(frac*nbrowser,0)):len(uaslist)+1]:
        tokens = [int(s)+1 for s in Tok.split(" ")]
        tokdict = {}
 #       for key in keys: tokdict[int(key)] = 0
        for tok in tokens: 
            if int(tok) < maxtok:
                try:
                    tokdict[int(tok)]
                except KeyError:
                    tokdict[int(tok)] = 1.0
                else:
                    tokdict[int(tok)] +=1.0
#        print tokdict    
        testData.append(('Browser', tokdict))
        testlist.append(uaString)
    print 'Number browsers selected for training: ', int(round(frac*nbrowser,0))    
    



# just select first 5000 elements of train data and first 1000 elements of test data
  #  random.shuffle(trainingData)    
  #  random.shuffle(testData)
  #  trainingData = trainingData[0:10000]
  #  testData = testData[0:1000]

# Make a Decision Problem
    params = LinearSVMParams()
    params.kernelName = "RBF"
    params.gamma = gamma
    params.C = C
    decProb = DecisionProblem("Type", params)
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

# get path for model
    filename = decProb.modelPath()
    print 'Filename: ', filename
    print 'saving model'
    svm_save_model(filename,model)
    labelfile = filename+'.labels'
    flabel = open(labelfile,'w')
    for i,label in enumerate(set(decProb.labels)):
        s = label + ':' + str(i) + '\n'
        flabel.write(s)

    flabel.close()
    ytest, xtest = decProb.makedata(testData)
    pred_labels, (ACC,MSE,SCC), pred_values = svm_predict(ytest,xtest,model)
# Predict
    correct = 0.0
    total = 0.0
    correct0 = 0.0
    correct1 = 0.0
    false1 = 0.0
    false0 = 0.0
    ind = 0
    fmiss = open('misclass.txt','w')
    for i, actual  in enumerate(ytest):
#        prediction = decProb.decide(ua)
        prediction = pred_labels[i]
        #if( actual == 'Robot'):
        if (actual == 0):
            if(actual == prediction):
                correct0 = correct0 + 1.0
                correct = correct + 1.0
            else:
                false1 = false1 + 1.0
                fmiss.write('false Browser: ' + testlist[ind]+'\n')
        #elif( actual == 'Browser'):
        elif (actual == 1):
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
    f.write(str(decProb.labelMap)+'\n')
    s = "ACCURACY: " + str(correct/total) + '\n'
    s = s + "False X means classifier said data was X, but it was actually something else\n"
    s = s + "Correct 0: " + str(correct0) + " False 0: " + str(false0) + '\n'
    s = s + "Correct 1: " + str(correct1) + " False 1: " + str(false1) + '\n'
    f.write(s)
    accuracy = correct/total    
    return accuracy,correct0,false0,correct1,false1

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print "You need to specify C, gamma space delimited"
        sys.exit(2)
    C = float(sys.argv[1])
    gamma = float(sys.argv[2])
    #runSVMlinear(C)
    runSVMlinear(C,gamma)
