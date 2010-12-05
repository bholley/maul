import random
from MaulParams import MaulParams
from MaulDataset import MaulDataset

#
# Top-Level Harness For Maul
#

# Parameters
params = MaulParams()
params.kernelName = 'linear'
params.dataType = 'vector'

# Random Seed
random.seed(18283835)

# Initialize a dataset
dataset = MaulDataset('mydb', params)
#dataset.crossValidate('Type', 0.8, 1.0, "WHERE (Type = 'Browser' OR Type = 'Robot')")
#dataset.crossValidate('Family', 0.8, 1.0, "WHERE (Type = 'Browser' AND Family IS NOT NULL)")
dataset.crossValidate('OS',0.8,1.0,"WHERE (Type = 'Browser' AND OS IS NOT NULL)")
