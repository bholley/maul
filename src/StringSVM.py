from ctypes import *
import platform

class StringSVM:

  labels = []
  strings = []

  finalized = False

  def __init__(self):

    # Load libSVM
	if platform.system() == "Windows":
		self.svmlib = cdll.LoadLibrary("../libsvm-string/libsvm-string-win32.dll");#WIN32
	else:
		self.svmlib = cdll.LoadLibrary("../libsvm-string/libsvm.so.2");# *NIX
    # Set the prototypes on the functions we care about

	self.svmlib.svm_train.restype = POINTER(svm_model)
	self.svmlib.svm_train.argtypes = [POINTER(svm_problem), POINTER(svm_parameter)]
	self.svmlib.svm_predict_p.restype = c_double
	self.svmlib.svm_predict_p.argtypes = [POINTER(svm_model), POINTER(svm_data)]
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

  # Takes a single sample and stores it
  def addSample(self, label, string):
    self.labels.append(label)
    self.strings.append(string)


  # Finalizes the training data. No more data may be added
  def finalize(self):

    # Validate
    if not self.strings:
      raise RuntimeError("No training data!")

    # Generate a mapping from string labels to numbers
    self.labelMap = dict()
    self.reverseLabelMap = dict()
    for i, label in enumerate(set(self.labels)):
      self.labelMap[label] = i
      self.reverseLabelMap[i] = label

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

    # Generate the parameters
    params = svm_parameter()

    # Generate the model
    self.model = self.svmlib.svm_train(problem, params)

  def predict(self, string):

    # Validate
    if not hasattr(self, 'model'):
      raise RuntimeError("Need to call train() first!")

    # Make a prediction
    query = svm_data()
    query.v = None
    query.s = string
    prediction = self.svmlib.svm_predict_p(self.model, pointer(query))

    return self.reverseLabelMap[int(prediction)]

"""
Python Wrappers for C Data Structures

These inherit special magic from ctypes.Structure
"""
SVM_TYPE_C_SVC = 0
KERNEL_TYPE_STRING = 5
DATA_TYPE_STRING = 1
class svm_parameter(Structure):
  _fields_ = [("svm_type", c_int),
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
  def __init__(self):
    Structure.__init__(self)
    self.svm_type = SVM_TYPE_C_SVC
    self.kernel_type = KERNEL_TYPE_STRING
    self.data_type = DATA_TYPE_STRING
    self.degree = 3
    self.gamma = 0.1
    self.coef0 = 0
    self.cache_size = 100
    self.eps = 1e-3
    self.C = 1
    self.nr_weight = 0
    self.weight_label = None
    self.weight = None
    self.nu = 0.5
    self.p = 0.1
    self.shrinking = 1
    self.probability = 0



class svm_model(Structure):
  _fields_ = []

class svm_data(Structure):
  _fields_ = [("v", c_void_p), # This is actually a pointer to an svm_node, but
                              # it's always null for string operation.
              ("s", c_char_p)]

class svm_problem(Structure):
  _fields_ = [("l", c_int),
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
      self.x[i].v = None
      self.x[i].s = string

