from ctypes import *

class StringSVM:

  labels = []
  strings = []

  finalized = False

  def __init__(self):

    # Load libSVM
    self.svmlib = cdll.LoadLibrary("../libsvm-string/libsvm.so.2");

    # Set the prototypes on the functions we care about
    self.svmlib.svm_train.restype = POINTER(svm_model)
    self.svmlib.svm_train.argtypes = [POINTER(svm_problem), POINTER(svm_parameter)]
    self.svmlib.svm_free_and_destroy_model.restype = None
    self.svmlib.svm_free_and_destroy_model.argtypes = [POINTER(POINTER(svm_model))]

  def __del__(self):
    if self.model:
      self.svmlib.svm_free_and_destroy_model(pointer(self.model))

  # Takes a list of (string, string) tuples, and stores them
  def addSamples(self, samples):
    newLabels, newStrings = zip(*samples)
    self.labels = self.labels + list(newLabels)
    self.strings = self.strings + list(newStrings)


  # Finalizes the training data. No more data may be added
  def finalize(self):

    # Validate
    if not self.strings:
      raise RuntimeError("No training data!")

    # Generate a mapping from string labels to numbers
    self.labelMap = dict()
    for i, label in enumerate(set(self.labels)):
      self.labelMap[label] = i

    # Generate a numerical label list
    self.labelsNumeric = map(lambda x : self.labelMap[x], self.labels)

    # Flag that we're finalized
    self.finalized = True

  def train(self):

    # Validate
    if (hasattr(self, 'model')):
      raise RuntimeError("Already have a model!")
    if (not self.finalized):
      raise RuntimeError("Must call finalize() before calling train()!")

    # Generate the problem
    problem = svm_problem(self.labelsNumeric, self.strings)
    params = svm_parameter()

    # Generate the model
    self.model = self.svmlib.svm_train(problem, params)

"""
Python Wrappers for C Data Structures

These inherit special magic from ctypes.Structure
"""
class svm_parameter(Structure):
  _fields = [("svm_type", c_int),
             ("data_type", c_int),
             ("kernel_type", c_int),
             ("degree", c_int),
             ("gamma", c_double),
             ("coef0", c_double),
             ("cache_size", c_double),
             ("eps", c_double),
             ("C", c_double),
             ("nr_weight", c_int),
             ("weight_label", POINTER(c_int)),
             ("weight", POINTER(c_double)),
             ("nu", c_double),
             ("p", c_double),
             ("shrinking", c_int),
             ("probability", c_int)]

class svm_model(Structure):
  _fields = []

class svm_data(Structure):
  _fields = [("v", c_void_p), # This is actually a pointer to an svm_node, but
                              # it's always null for string operation.
             ("s", c_char_p)]

class svm_problem(Structure):
  _fields = [("l", c_int),
             ("y", POINTER(c_double)),
             ("x", POINTER(svm_data))]

  def __init__(self, labels, strings):

    # Validate
    if (len(labels) != len(strings)):
      raise ValueError("Need equal number of strings and labels!")

    # Set the length
    self.l = len(labels)

    # Set the labels
    #
    # According to the ctypes tutorial, "The recommended way to create array
    # types is by multiplying a data type with a positive integer". Um, ok...
    self.y = (c_double * self.l)()
    for i, label in enumerate(labels): self.y[i] = label

    # Set the strings
    self.x = (svm_data * self.l)()
    for i, string in enumerate(strings):
      self.x.v = None
      self.x.s = string

