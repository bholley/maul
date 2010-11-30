import sys, os, re
sys.path.append('../src/')
sys.path.append('../data-raw/')
from uaobj import *
from merge_data import dsort,dictsortprintfile,writestat,descriptivestat



def main():
    ualist = readFile('uadata_clean_token.txt')

# merge Robot and Validator class    
    for x in ualist:
        try:
            x.data['Type']
        except KeyError:
            continue
        else:
            if(x.data['Type']=="Validator"):
                x.data['Type'] = "Robot"

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

