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
params.coef0 = 1

# Random Seed
random.seed(18283835)

# Initialize a dataset
#dataset = MaulDataset('../data/maul.db', params)
#dataset.crossValidate('Type', 0.8, 1.0, "WHERE (Type = 'Browser' OR Type = 'Robot')")
#dataset.crossValidate('Family', 0.8, 1.0, "WHERE (Type = 'Browser' AND Family IS NOT NULL)")
#dataset.crossValidate('OS',0.8,1.0,"WHERE (Type = 'Browser' AND OS IS NOT NULL)")
#dataset.crossValidate('Type', 0.8, 1.0, "WHERE (Type = 'Browser' OR Type = 'Robot' OR Type = 'Mobile Browser')")




# playing with hard to classify strings
dataset = MaulDataset('../data/maul.db.excl', params) # load DB which excluded the hard to classify  strings
# train on all of the dataset
dataset.crossValidate('Type', 1.0, 1.0, "WHERE (Type = 'Browser' OR Type = 'Robot' OR Type = 'Mobile Browser')")


# load nasty strings
testset = MaulDataset('../data/nastydb',params)
testset.loadSamples('Type',"WHERE (Type = 'Browser' OR Type = 'Robot' OR Type = 'Mobile Browser')")

# format into same way prediction is run inside
sampleList = list()
for key in testset.samples.keys():
    sampleList.extend(testset.samples[key])

# predict and output results
for sample in sampleList:
    prepared = testset.prepareSample(sample)
    prediction = dataset.problem.decide(prepared[1])
    print 'pred: ', prediction, ' actual: ', sample['label']
    print sample['uaString']



