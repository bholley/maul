import os, sys, re
sys.path.append('../src/')
from uaobj import *



def main():
	ualist = readFile('uadata.txt') # read in data
	f = open('unparsed.txt','w')
	for x in ualist:
		if not x.data:
			f.write(x+'\n')
	f.close()
	return 0

if __name__ == "__main__":
	main()
