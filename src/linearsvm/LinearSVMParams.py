'''Class encapsulating relevant SVM parameters'''

class LinearSVMParams:

  def __init__(self):

    # Set some reasonable defaults
    self.kernelName = 'linear'
    self.C = 1
    self.gamma = 0.1
    self.degree = 3
    self.coef0 = 0


  '''Generates a canonical representation of the parameters as a string'''
  def toString(self):

    # Kernel Name
    rv = self.kernelName
    rv = rv + "_C-" + str(self.C) 
    if self.kernelName == "RBF":
        rv = rv + "_gamma-"+str(self.gamma)
    elif self.kernelName == "poly":
        rv = rv + "_degree-"+str(self.degree)
        rv = rv + "_coef0-"+str(self.coef0)


    # All done
    return rv
