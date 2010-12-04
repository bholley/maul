from MaulSVM import MaulSVM
import os

'''This class encapsulates a single decision problem.'''


class MaulProblem:

  def __init__(self, category, params):

    # Basic Initialization
    self.category = category
    self.params = params
    self.svm = None


  def decide(self, ua):

    if not self.svm:
      raise RuntimeError("Can't make decision without a model!")

    # UA will be either a string or a token array. We're agnostic
    # to which one it is at this level in the code.
    return self.svm.predict(ua)

  ''' Trains an SVM, generating a live model. '''
  def generateModel(self, samples):

    # Instantiate an SVM
    self.svm = StringSVM(self.params)

    # Train it
    self.svm.addSamples(samples)
    self.svm.finalize()
    self.svm.train()

  ''' Saves the model. '''
  def saveModel(self):

    # If a directory for this category doesn't exist, make one
    if not os.path.isdir(self.modelBasePath()):
      os.makedirs(self.modelBasePath())

    # Save the model
    self.svm.svm_save_model(self.modelPath())

  ''' Loads a model from disk. '''
  def loadModel(self):

    if not self.haveModel():
      raise RuntimeError("Can't load nonexistant model!")

    # Make an SVM
    self.svm = StringSVM(self.params)

    # Load the model
    self.svm.svm_load_model(self.modelPath())

  ''' Checks whether a model has been generated. '''
  def haveModel(self):

    return os.path.isfile(self.modelPath())

  ''' Generates the path of the model file for this problem. '''
  def modelPath(self):

    return self.modelBasePath() + '/' + self.params.toString() + '.model'

  def modelBasePath(self):

    return 'models/' + self.category
