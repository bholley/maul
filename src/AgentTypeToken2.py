from StringSVM import StringSVM
from SVMParams import SVMParams
import sqlite3
import random

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

# bots
c.execute('select Tokens from data where "Type" = "Robot"')
uaslist = []
for uaString in c:
    uaslist.append(uaString[0])
nrobot = len(uaslist)
random.shuffle(uaslist)
for uaString in uaslist[0:int(round(frac*nrobot,0))]:
    tokens = [int(s) for s in uaString.split(" ")]
    trainingData.append(('Robot', tokens))
for uaString in uaslist[int(round(frac*nrobot,0)):len(uaslist)+1]:
    tokens = [int(s) for s in uaString.split(" ")]
    testData.append(('Robot', tokens))
print 'Number robots selected for training: ', int(round(frac*nrobot,0))

# browsers
c.execute('select Tokens from data where "Type" = "Browser"')
uaslist = []
for uaString in c:
    uaslist.append(uaString[0])
nbrowser = len(uaslist)
random.shuffle(uaslist)
for uaString in uaslist[0:int(round(frac*nbrowser,0))]:
    tokens = [int(s) for s in uaString.split(" ")]
    trainingData.append(('Browser', tokens))
for uaString in uaslist[int(round(frac*nbrowser,0)):len(uaslist)+1]:
    tokens = [int(s) for s in uaString.split(" ")]
    testData.append(('Browser', tokens))
print 'Number browsers selected for training: ', int(round(frac*nbrowser,0))    
    
# just select first 5000 elements of train data and first 1000 elements of test data
random.shuffle(trainingData)    
random.shuffle(testData)
#trainingData = trainingData[0:10000]
#testData = testData[0:2000]


# Make a StringSVM
params = SVMParams()
params.kernelName = "subseq"
params.tokenized = True
svm = StringSVM(params)

# Train
svm.addSamples(trainingData)
svm.finalize()
svm.train()

# Predict
correct = 0.0
total = 0.0
correct0 = 0.0
correct1 = 0.0
false1 = 0.0
false0 = 0.0
for actual, ua in testData:
  prediction = svm.predict(ua)
  if( actual == 'Robot'):
    if(actual == prediction):
        correct0 = correct0 + 1.0
        correct = correct + 1.0
    else:
          false1 = false1 + 1.0
  elif( actual == 'Browser'):
    if(actual == prediction):
        correct1 = correct1 + 1.0
        correct = correct+1.0
    else:
        false0 = false0 + 1.0
    
  total = total + 1.0

print "ACCURACY: ", correct / total
print "False X means classifier said data was X, but it was actually something else"
print "Correct Robot: ", correct0, "False Robot: ", false0
print "Correct Browser: ", correct1, "False Browser: ", false1

# save the model for use later
svm.svm_save_model('agenttype.model')




# RESULTS FROM OUTPUT, SINCE MODEL ISN'T SAVED
# used seed above
#iter 2157
#nu = 0.008741
# obj = -295.857291, rho = 1.000092
# nSV = 917, nBSV = 311
# total nSV = 917
# Accuracy = 0.992677110629
# Correct Robot: 383.0 False Robot: 72.0
# Correct Browser: 9918.0  False Browser: 4.0

