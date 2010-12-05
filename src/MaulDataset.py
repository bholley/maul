from MaulProblem import MaulProblem
import sqlite3
import random

class MaulDataset:

  # Constructor
  def __init__(self, dbName, params):

    # Store Params
    self.params = params
    self.dbName = dbName

  # Standard Cross-Validation Routine
  def crossValidate(self, category, trainingProportion, totalProportion, constraints):

    # Open Database
    conn = sqlite3.connect(self.dbName)
    conn.text_factory = str
    c = conn.cursor()

    # Query
    # TODO - respect constraints
    c.execute('select uaString, Tokens, ' + category + ' from data ' + constraints)

    # Organize our samples by label (tracking the maximum token while we do it)
    self.maxToken = 0
    samples = dict()
    for item in c:
      label = item[2]
      uaString = item[0]
      tokens = [int(s) for s in item[1].split(' ')]
      self.maxToken = max(self.maxToken, max(tokens))
      if not samples.has_key(label):
        samples[label] = []
      samples[label].append({"uaString" : uaString, "tokens": tokens, "label" : label})

    # Process the data to extract training data (everything that remains
    # is test data)
    trainingData = []
    for key in samples.keys():

      # Shuffle the data
      random.shuffle(samples[key])

      # If we want to use less than our total amount of data (for speed),
      # shrink the list now
      if totalProportion < 1.0:
        del samples[key][int(len(samples[key]) * totalProportion):]

      # Pick out training data
      for i in range(1, int(len(samples[key]) * trainingProportion)):
        trainingData.append(self.prepareSample(samples[key].pop()))

    # Make a decision problem
    problem = MaulProblem(category, self.params)

    # If the model is not already generated, generate it
    if not problem.haveModel():
      problem.generateModel(trainingData)
      problem.saveModel()
    else:
      problem.loadModel()


  # Helper routine to put a sample in the format MaulSVM expects given
  # the problem parameters
  def prepareSample(self, sample):

    if self.params.dataType == "string":
      return (sample["label"], sample["uaString"])
    elif self.params.dataType == "tokens":
      return (sample["label"], sample["tokens"])
    elif self.params.dataType == "vector":
      vec = [0] * self.maxToken
      for i in sample["tokens"]:
        vec[i] += 1
      return (sample["label"], vec)
    else:
      raise ValueError("Unknown datatype: " + str(self.params.dataType))
