'''Class encapsulating relevant SVM parameters'''

class SVMParams:

  def __init__(self):

    # Set some reasonable defaults
    self.kernelName = 'edit'
    self.tokenized = False
    self.seqLambda = 0.8
    self.seqLen = 5
    self.C = 1


  '''Generates a canonical representation of the parameters as a string'''
  def toString(self):

    # Kernel Name
    rv = self.kernelName
    rv = rv + "_C-" + str(self.C) 
    # Tokenized?
    if (self.tokenized):
      rv = rv + "_" + "tokenized"
    else:
      rv = rv + "_" + "untokenized"

    # Subseq Params
    if (self.kernelName == "subseq"):
      rv = rv + "_lambda-" + str(self.seqLambda)
      rv = rv + "_seqlen-" + str(self.seqLen)

    # All done
    return rv
