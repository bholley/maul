import sys
sys.path.append('../src/')
from uaobj import *



def main():
	ualist1 = readFile('csvdata.txt')
	print 'Loaded csvdata.txt'
	print 'UA List 1 has length, ', len(ualist1)
	ualist2 = readFile('xmldata.txt')
	print 'Loaded xmldata.txt'	
	print 'UA List 2 has length, ', len(ualist2)

	ualist, newentries = mergelists(ualist1,ualist2)
	print 'Newentries, ', newentries	
	print 'Total Entries,', len(ualist)

# generate dictionaries of categories
# 	output new list
	f = open('../data/uadata.txt','w')

	osdict = {}
	typdict = {}
	familydict = {}
	osversiondict = {}

	for (i,x) in enumerate(ualist):
		if 'OS' in x.data:
			osdict[x.data['OS']] = i
		if 'Family' in x.data:
			familydict[x.data['Family']] = i
		if 'Type' in x.data:
			typdict[x.data['Type']] = i
		if 'OS Version' in x.data:
			osversiondict[x.data['OS Version']] = i
		f.write(x+'\n')
			

	f.close()	

	fosversion = open('../data/osversion.txt','w')
	fos = open('../data/os.txt','w')
	ftyp = open('../data/types.txt','w')
	ffamily = open('../data/families.txt','w')
	for k in osdict.keys():
		fos.write(k+'\n')
	for k in typdict.keys():
		ftyp.write(k+'\n')
	for k in familydict.keys():
		ffamily.write(k+'\n')
	for k in osversiondict.keys():
		fosversion.write(k+'\n')
	fosversion.close()
	fos.close()
	ftyp.close()
	ffamily.close()


def mergelists(ualist1,ualist2):
	ualist = ualist1
	cnt = 0
	for x in ualist2:
		hit = 0
		for y in ualist1:
			if x.uaString == y.uaString:
				hit = 1
		if hit == 0:
			ualist.append(x)
			cnt = cnt +1
	return ualist, cnt
if __name__=="__main__":
	main()
