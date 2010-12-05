import random
from MaulParams import MaulParams
from MaulDataset import MaulDataset

#
# Top-Level Harness For Maul
#

# Parameters
params = MaulParams()
params.kernelName = 'edit'
params.dataType = 'tokens'

# Random Seed
random.seed(18283835)

# Initialize a dataset
dataset = MaulDataset('mydb', params)
#dataset.constrain('Type', 'Browser')
dataset.crossValidate('Type', 0.8, 0.1, "WHERE (Type = 'Browser' OR Type = 'Robot')")
