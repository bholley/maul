from StringSVM import StringSVM
import sqlite3
import random

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
c.execute('select uaString from data where "Type" = "Robot"')
uaslist = []
for uaString in c:
    uaslist.append(uaString[0])
nrobot = len(uaslist)
random.shuffle(uaslist)
for uaString in uaslist[0:int(round(frac*nrobot,0))]:
    trainingData.append(('Robot',uaString))
for uaString in uaslist[int(round(frac*nrobot,0)):len(uaslist)+1]:
    testData.append(('Robot',uaString))
print 'Number robots selected for training: ', int(round(frac*nrobot,0))

# browsers
c.execute('select uaString from data where "Type" = "Browser"')
uaslist = []
for uaString in c:
    uaslist.append(uaString[0])
nbrowser = len(uaslist)
random.shuffle(uaslist)
for uaString in uaslist[0:int(round(frac*nbrowser,0))]:
    trainingData.append(('Browser',uaString))
for uaString in uaslist[int(round(frac*nbrowser,0)):len(uaslist)+1]:
    testData.append(('Browser',uaString))
print 'Number browsers selected for training: ', int(round(frac*nbrowser,0))    
    
# just select first 5000 elements of train data and first 1000 elements of test data
random.shuffle(trainingData)    
random.shuffle(testData)
trainingData = trainingData[0:500]
testData = testData[0:100]


# Make a StringSVM
svm = StringSVM("edit")

# Train
#svm.addSamples(trainingData)
#svm.finalize()
#svm.train()

# load model
svm.svm_load_model('agenttype.model')


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



