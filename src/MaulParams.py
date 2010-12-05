'''Class encapsulating relevant Maul parameters'''

class MaulParams:

  def __init__(self):

    # Set some reasonable defaults
    self.kernelName = 'edit'
    self.dataType = "string"
    self.C = 1
    self.gamma = 0.1

    # Subsequence only
    self.seqLambda = 0.8
    self.seqLen = 5

    # Vector only
    self.coef0 = 0
    self.degree = 3


  '''Generates a canonical representation of the parameters as a string'''
  def toString(self):

    # Kernel Name
    rv = self.kernelName
    rv = rv + "_C-" + str(self.C) 
    rv = rv + "_" + self.dataType

    # Subseq Params
    if (self.kernelName == "subseq"):
      rv = rv + "_lambda-" + str(self.seqLambda)
      rv = rv + "_seqlen-" + str(self.seqLen)
    if(self.kernelName == "edit"):
        rv = rv + "_gamma-"+str(self.gamma)
    # All done
    return rv
