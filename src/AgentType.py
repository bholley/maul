from StringSVM import StringSVM
import sqlite3
import random

# Throwaway test to classify browser vs bot

# Open the database
conn = sqlite3.connect("mydb")
conn.text_factory = str
c = conn.cursor()

# Data
trainingData = [];
testData = [];

# bots
c.execute('select uaString from data where "Type" = "Robot"')
for uaString in c:
  if (random.random() < 0.8):
    trainingData.append(('Robot', uaString[0]))
  else:
    testData.append(('Robot', uaString[0]))

# browsers
c.execute('select uaString from data where "Type" = "Browser"')
for uaString in c:
  if (random.random() < 0.8):
    trainingData.append(('Browser', uaString[0]))
  else:
    testData.append(('Browser', uaString[0]))


# just select first 5000 elements of train data and first 1000 elements of test data
trainingData = trainingData[0:5000]
testData = testData[0:1000]


# Make a StringSVM
svm = StringSVM()

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
