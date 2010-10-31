import re
from uasparser import UASparser

class uaobject:
	def __init__(self):
		self.uastring = str()
		self.typ = str() 
		self.family = str()
		self.name = str()
		self.engine = str()
		self.versiontype = str()
		self.versionnumber = str()
		self.build = str()
		self.cputype = str()
		self.arch = str()
		self.os = str()
		self.osversion = str()
		self.botversion = str()
	def getstring(self):
		r = self.uastring + '\n'
		if self.typ != "": 
			r = r + "Type: " + self.typ+ '\n'
		if self.engine != "":
			r = r + "Engine: " + self.engine + '\n'
		if self.family != "":
			r = r + "Family: " + self.family + '\n'
		if self.name != "":
			r = r + "Name: " + self.name + '\n'
		if self.versiontype != "":
			r = r + "Version Type: " + self.versiontype + '\n'
		if self.versionnumber != "":
			r = r + "Version Number: " + self.versionnumber + '\n'
		if self.build != "":
			r = r + "Build: " + self.build + '\n'
		if self.cputype != "":
			r = r + "CPU Type: " + self.cputype + '\n'
		if self.arch != "":
			r = r + "Arch: " + self.arch + '\n'
		if self.os != "":
			r = r + "OS: " + self.os + '\n'
		if self.osversion != "":
			r = r + "OS Version: " +self.osversion + '\n'
		if self.botversion != "":
			r = r + "Bot Version: " + self.botversion + '\n'
		return r
	def __str__(self):
		r = self.getstring()
		return r

def main():
# start with OS file
	f = open('uasOS_example_20101014-01.csv')
	ualist = list()
	for (i,line) in enumerate(f):
		m = re.split(r"\",",line)
		m[0] = m[0].replace('"','') # clean up quotes
		m[1] = m[1].replace('"','')
		m[1] = m[1].replace('\n','')
		x = uaobject()
		x.uastring = m[1];
# pull in parse from parser on ua-string-info.com
		ualist.append(x)	
	print "number of ua strings from OS file " + str(i)	
# now load other file, compare strings as well
	f = open('uas_example_20101014-01.csv')
	newcnt = 0
	for (i,line) in enumerate(f):
		m = re.split(r"\",",line)
		m[0] = m[0].replace('"','') # clean up quotes
		m[0] = m[0].lower()
		m[1] = m[1].replace('"','')
		m[2] = m[2].replace('\n','')
		m[2] = m[2].replace('"','')
		hit = 0
		for (j,x) in enumerate(ualist):
			if x.uastring == m[2]:
				hit = 1
				break
		if hit == 0:
			newcnt = newcnt+1
			x = uaobject()
			x.uastring = m[2]
			ualist.append(x)
	print "number of new ua strings main example file " + str(newcnt)	
# now bring in bot csv file	 THERE ARE NO NEW STRINGS IN BOT FILE
#	f = open('botIP.csv')	
#	newcnt = 0
#	for (i,line) in enumerate(f):
#		m = re.split(r"\",",line)
#		m[0] = m[0].replace('"','')
#		m[5] = m[5].replace('"','')
#		m[6] = m[6].replace('"','')
#		m[6] = m[6].replace('\n','')
#		hit = 0
#		for (j,x) in enumerate(ualist):
#			if x.uastring == m[6]:
#				hit = 1
#				break
#		if hit == 0:
#			newcnt = newcnt+1
#			x = uaobject()
#			x.uastring = m[6]
#			ualist.append(x)
#	print "number of new UAs in botIP.csv: " + str(newcnt)
	
	uas_parser = UASparser()
	osdict = {}
	typdict = {}
	familydict = {}
	osversiondict = {}
	# also make unique only list of all properties
	for (i,x) in enumerate(ualist):
#		if i > 10:
#			break
		print "parsing UA string ", i
		result = uas_parser.parse(x.uastring)
		[ostype,osversion] = osparse(result['os_name'])

		if result['typ'] != 'unknown':
			x.typ = result['typ']
			typdict[x.typ] = i
		if result['ua_family'] != 'unknown':	
			x.family = result['ua_family']
			familydict[x.family] = i
		if ostype != 'unknown': 
			x.os = ostype
			osdict[x.os] = i
		if osversion != '':
			x.osversion = osversion
			osversiondict[x.osversion] = i

	f = open('../data/uadata.txt','w')		
	fos = open('../data/os.txt','w')
	ftyp = open('../data/types.txt','w')
	ffamily = open('../data/families.txt','w')
	fosversion = open('../data/osversion.txt','w')
	for k in osdict.keys():
		fos.write(k+'\n')
	for k in typdict.keys():
		ftyp.write(k+'\n')
	for k in familydict.keys():
		ffamily.write(k+'\n')
	for k in osversiondict.keys():
		fosversion.write(k+'\n')
	for x in ualist:
		f.write(x.getstring()+ '\n')
	ftyp.close()
	ffamily.close()
	fos.close()
	fosversion.close()
	f.close()
	return 0


def osparse(osstring):
	if( osstring == 'Windows XP'):
		ostype = 'Windows'
		osversion = 'XP'
	elif(osstring == 'Windows 2003 Server'):
		ostype = 'Windows'
		osversion = '2003 Server'
	elif(osstring == 'Windows 7'):
		ostype = 'Windows'
		osversion = '7'
	elif(osstring == 'Windows 95'):
		ostype = 'Windows'
		osversion = '95'
	elif(osstring == 'Windows Phone 7'):	
		ostype = 'Windows Phone 7'
		osversion = ''
	elif(osstring == 'Windows ME'):
		ostype = 'Windows'
		osversion = 'ME'
	elif(osstring == 'Windows'):
		ostype = 'Windows'
		osversion = ''
	elif(osstring == 'Windows'):
		ostype = 'Windows Mobile'
		osversion = ''
	elif(osstring == 'Windows NT'):
		ostype = 'Windows'
		osversion = 'NT'
	elif(osstring == 'Windows 3.x'):
		ostype = 'Windows'
		osversion = '3.x'
	elif(osstring == 'Windows Vista'):
		ostype = 'Windows'
		osversion = 'Vista'
	elif(osstring == 'Windows 2000'):
		ostype = 'Windows'
		osversion = '2000'
	elif(osstring == 'Windows 98'):
		ostype = 'Windows'
		osversion = '98'
	elif(osstring == 'Windows CE'):
		ostype = 'Windows'
		osversion = 'CE'
	elif(osstring.find('Linux') != -1):	
		if(osstring == 'Linux'):
			ostype = 'Linux'
			osversion = ""
		else:
			m = re.search(r"(\w+) \((\w+)\)",osstring)
			try:
				ostype = m.group(1)
				osversion = m.group(2)
			except:
				m = re.search(r"(\w+) \((\w+)\s(\w+)\)",osstring)
				ostype = m.group(1)
				osversion = m.group(2) + ' ' + m.group(3)
	else:	
		ostype = osstring
		osversion = ""

	return ostype,osversion


if __name__ == "__main__":
	main()
