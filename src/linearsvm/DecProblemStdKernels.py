#from LinearSVM import *
import os

'''This class encapsulates a single decision problem.'''


class DecisionProblem:

  def __init__(self, category, params):

    # Basic Initialization
    self.category = category
    self.params = params
    self.labels = []
    self.values = []

  def makedata(self,trainingData):
    self.labels, self.values = zip(*trainingData) 
    self.labelMap = dict()
    self.reverseLabelMap = dict()
    for i, label in enumerate(set(self.labels)):
        self.labelMap[label] = i
        self.reverseLabelMap[i] = label
    self.labelsNumeric = map(lambda x : float(self.labelMap[x]), self.labels)

    return self.labelsNumeric, self.values


  def maketest(self, testData):
    ylab, values = zip(*testData)
    ytest = map(lambda x : float(self.labelMap[x]), ylab)
    return ytest, values
  
  def genoptions(self):
    options = str()
#    if self.params.kernelName == "linear":
    options += "-s 0" # SELECT C-SVM
    if self.params.kernelName == "linear":
        options += " -t 0"
    elif self.params.kernelName == "RBF":
        options += " -t 2"
        gammastr = str(float(self.params.gamma))
        options += " -g " + gammastr
    elif self.params.kernelName == "poly":
        options += " -t 1"
        degreestr = str(int(self.params.degree))
        options += " -d " + degreestr
        coef0str = str(float(self.params.coef0))
        options += " -r " + coef0str
    cstr = str(float(self.params.C))    
    options += " -c " + cstr
    options += " -h 1"
    return options

  ''' Checks whether a model has been generated. '''
  def haveModel(self):

    return os.path.isfile(self.modelPath())

  ''' Generates the path of the model file for this problem. '''
  def modelPath(self):
#    return 'decproblemodel.model'
    return self.modelBasePath() + '/' + self.params.toString() + '.model'

  def modelBasePath(self):

    return 'models/' + self.category
