import random
import os
from MaulParams import MaulParams
from MaulDataset import MaulDataset

#
# Top-Level Batch Harness For Maul
#

def writeResults(params, testName, results):

  # Open our file
  targetDir = 'results/' + testName
  if not os.path.isdir(targetDir):
    os.makedirs(targetDir)
  file = open(targetDir + '/' + params.toString(), 'w')

  # Write our output
  file.write('Test Name: ' + testName + '\n')
  file.write('Kernel: ' + params.kernelName + '\n')
  file.write('Data Type: ' + params.dataType + '\n')
  file.write('Canonical Parameter String: ' + params.toString() + '\n')
  file.write('\n')
  file.write('ACCURACY: ' + str(results['correct'] / results['total']))
  file.write(' (' + str(int(results['correct'])) + '/' + str(results['total']) + ')\n')
  file.write('\n')
  file.write('False Positives:\n')
  file.write(str(results['falsePositives']))
  file.write('\n\n')
  file.write('False Negatives:\n')
  file.write(str(results['falseNegatives']))
  file.write('\n\n')
  file.write('Misses:\n')
  for miss in results['misses']:
    file.write(miss + '\n')

  # Done
  file.close()



# Define parameter combinations
kernelAndType = [('linear', 'vector'),
                 ('RBF', 'vector'),
                 ('edit', 'tokens'),
                 ('subseq', 'tokens')]
testAndQuery = [('Type', "WHERE (Type = 'Browser' OR Type = 'Robot'"\
                         " OR Type = 'Mobile Browser')"),
                ('OS', "WHERE (Type = 'Browser' AND OS IS NOT NULL)"),
                ('Family', "WHERE (Type = 'Browser' AND Family IS NOT NULL)")]

# Iterate over parameter possibilities:
for kernel, type in kernelAndType:
  for test, query in testAndQuery:

    # Parameters
    params = MaulParams()
    params.kernelName = kernel
    params.dataType = type

    # Random Seed
    random.seed(18283835)

    # Initialize a dataset
    dataset = MaulDataset('mydb', params)

    # Run cross-validation
    results = dataset.crossValidate(test, 0.8, 1.0, query)

    # Print results
    writeResults(params, test, results)
