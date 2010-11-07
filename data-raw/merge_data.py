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
	ualist3 = readFile('uatrack_data.txt')
	print 'Loaded uatracker data'
	print 'UA List 3 has length, ', len(ualist3)

	print 'Merging UAList 1 and UAList 2'
	ualist, newentries = mergelists(ualist1,ualist2)
	print 'Newentries, ', newentries	
	print 'Total Entries,', len(ualist)

	print 'Merging UaList 3 and Rest'
	ualist, newentries = mergelists(ualist,ualist3)
	print 'Newentries ', newentries
	print 'Total Entries,', len(ualist)

# generate dictionaries of categories
# 	output new list
	f = open('../data/uadata.txt','w')

	for x in ualist:			
		f.write(x+'\n')

	f.close()	
	
	
	catdict, typdict, familydict, osdict, osversiondict =  descriptivestat(ualist)		
	
	fosversion = open('../data/osversion.txt','w')
	fos = open('../data/os.txt','w')
	ftyp = open('../data/types.txt','w')
	ffamily = open('../data/families.txt','w')
	fcat = open('../data/categories.txt','w')


	dictsortprintfile(osdict,fos)
	dictsortprintfile(typdict,ftyp)
	dictsortprintfile(familydict,ffamily)
	dictsortprintfile(osversiondict,fosversion)
	
	for k in catdict.keys():
		fcat.write(k+'\n')
	fosversion.close()
	fos.close()
	ftyp.close()
	ffamily.close()
	fcat.close()


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

def dsort(dic):
	items = [(v,k) for k,v in dic.items()]
	items.sort(reverse=True)
	return [k for (v,k) in items]

def dictsortprintfile(dic,fid):
	keysort = dsort(dic)
	for k in keysort:
		s = k + ", " + str(dic[k])
		fid.write(s + '\n')

def descriptivestat(ualist):
	osdict = {}
	typdict = {}
	familydict = {}
	osversiondict = {}
	catdict = {}

	for (i,x) in enumerate(ualist):
		if 'OS' in x.data:
			try:
				osdict[x.data['OS']] 
			except KeyError:
				osdict[x.data['OS']] = 1
			else:
				osdict[x.data['OS']] += 1
		if 'Family' in x.data:
			try:
				familydict[x.data['Family']] 
			except KeyError:
				familydict[x.data['Family']] = 1
			else:
				familydict[x.data['Family']] += 1
		if 'Type' in x.data:
			try:
				typdict[x.data['Type']] 
			except KeyError:
				typdict[x.data['Type']] = 1
			else:
				typdict[x.data['Type']] += 1
		if 'OS Version' in x.data:
			try:
				osversiondict[x.data['OS Version']] 
			except KeyError:
				osversiondict[x.data['OS Version']] = 1
			else:
				osversiondict[x.data['OS Version']] += 1
		for key in x.data.keys():
			catdict[key] = 1

	return catdict, typdict, familydict, osdict, osversiondict		
if __name__=="__main__":
	main()
