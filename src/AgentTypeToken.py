from StringSVM import StringSVM
import sqlite3
import random

# Throwaway test to classify browser vs bot

# Open the database
conn = sqlite3.connect("bigtoken")
conn.text_factory = str
c = conn.cursor()

# Data
trainingData = [];
testData = [];

# bots
c.execute('select uaString from data where "Type" = "Robot"')
for uaString in c:
  tokens = [int(s) for s in uaString[0].split(" ")]
  if (random.random() < 0.8):
    trainingData.append(('Robot', tokens))
  else:
    testData.append(('Robot', tokens))

# browsers
c.execute('select uaString from data where "Type" = "Browser"')
for uaString in c:
  tokens = [int(s) for s in uaString[0].split(" ")]
  if (random.random() < 0.8):
    trainingData.append(('Browser', tokens))
  else:
    testData.append(('Browser', tokens))


# just select first 5000 elements of train data and first 1000 elements of test data
trainingData = trainingData[0:5000]
testData = testData[0:1000]


# Make a StringSVM
svm = StringSVM(kernelName="subseq", tokenized=True)

# Train
svm.addSamples(trainingData)
svm.finalize()
svm.train()

# Predict
correct = 0.0;
total = 0.0;
for actual, ua in testData:
  prediction = svm.predict(ua)
  if (prediction == actual):
    correct = correct + 1.0
  total = total + 1.0

print correct / total
