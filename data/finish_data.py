import sys, os, re
sys.path.append('../src/')
sys.path.append('../data-raw/')
from uaobj import *
from merge_data import dsort,dictsortprintfile,writestat,descriptivestat

# Helper routine to replace x[fieldName] with _value_ if x[fieldName] exists
# and matches regexp
def replaceField(x, fieldName, regexp, value,fieldName2='',value2=''):
  try:
    x.data[fieldName]
  except KeyError:
    return
  if (re.match(regexp, x.data[fieldName])):
    x.data[fieldName] = value
    if not fieldName2 == '':
        x.data[fieldName2] = value2

# Helper routine to determine if a given x is a browser or not
def isBrowser(x):
  return x.data.has_key('Type') and x.data['Type'] == 'Browser'

def countKeyBrowser(ua,key,keydict):
    if isBrowser(ua) and ua.data.has_key(key):
        keytemp = ua.data[key]
        if not keydict.has_key(keytemp):
            keydict[keytemp] = 0
        keydict[keytemp] = keydict[keytemp] + 1    
    return keydict

def main():
    ualist = readFile('uadata_clean_token.txt')

    families = dict()
    oses = dict()
    for x in ualist:

        # Call Validators Robots
        replaceField(x, 'Type', 'Validator', 'Robot')

        # Call Firefox (Shiretoko) and friends Firefox
        replaceField(x, 'Family', 'Firefox \(\w*\)$', 'Firefox')
        # Get rid of "compatibility view"
        replaceField(x,'Family','IE 8.0 \(Compatibility View\)','IE','Family Version','8.0compat')

        families = countKeyBrowser(x, 'Family', families)
        oses = countKeyBrowser(x, 'OS', oses)
        # running count on OS
#        if isBrowser(x)  and x.data.has_key('OS'):
#            os = x.data['OS']
#            if not oses.has_key(os):
#                oses[os] = 0
#            oses[os] = oses[os] + 1    

        # Keep a running count on the families
#        if isBrowser(x) and x.data.has_key('Family'):
#          family = x.data['Family']
#          if not families.has_key(family):
#            families[family] = 0
#          families[family] = families[family] + 1
        
    # Coalesce infrequent families into a single 'Other' family
    familyCountCap = min(len(families), 30)
    familyList = sorted(families, key=families.get)
    familyList.reverse()
    mainFamilies = familyList[0:familyCountCap]
    print "To keep the problem tractable, MAUL will only try to identify the following families: " + str(mainFamilies)
    for x in ualist:
      if isBrowser(x) and x.data.has_key('Family'):
        if x.data['Family'] not in mainFamilies:
          x.data['Family'] = 'Other'
    
    
    # coalesce any OS' with only one example into 'Other'
    for x in ualist:
        if isBrowser(x) and x.data.has_key('OS'):
            if oses[x.data['OS']] <= 1:
                print x.data['OS'], ' has only 1 example, coalescing into Other' 
                x.data['OS'] = 'Other'


    fua = open('uadata_clean_token_finished.txt','w')
    for x in ualist:
        fua.write(x+'\n')

    writestat(ualist,'./')

if __name__ == "__main__":
    main()

