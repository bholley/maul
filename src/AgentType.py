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
c.execute('select uaString from data where "Agent Type" = "bot"')
for uaString in c:
  if (random.random() < 0.8):
    trainingData.append(('bot', uaString[0]))
  else:
    testData.append(('bot', uaString[0]))

# browsers
c.execute('select uaString from data where "Agent Type" = "browser"')
for uaString in c:
  if (random.random() < 0.8):
    trainingData.append(('browser', uaString[0]))
  else:
    testData.append(('browser', uaString[0]))

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
