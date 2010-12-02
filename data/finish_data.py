import sys, os, re
sys.path.append('../src/')
sys.path.append('../data-raw/')
from uaobj import *
from merge_data import dsort,dictsortprintfile,writestat,descriptivestat

# Helper routine to replace x[fieldName] with _value_ if x[fieldName] exists
# and matches regexp
def replaceField(x, fieldName, regexp, value):
  try:
    x.data[fieldName]
  except KeyError:
    return
  if (re.match(regexp, x.data[fieldName])):
    x.data[fieldName] = value


def main():
    ualist = readFile('uadata_clean_token.txt')

# merge Robot and Validator class    
    for x in ualist:

        # Call Validators Robots
        replaceField(x, 'Type', 'Validator', 'Robot')

        # Call Firefox (Shiretoko) and friends Firefox
        replaceField(x, 'Family', 'Firefox \(\w*\)$', 'Firefox')

#    for x in ualist:
#        try:
#            x.data['Type']
#        except KeyError:
#            continue
#        else:
#            print x.data['Type']

    

    fua = open('uadata_clean_token_finished.txt','w')
    for x in ualist:
        fua.write(x+'\n')

    writestat(ualist,'./')

if __name__ == "__main__":
    main()

