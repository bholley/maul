import elementtree.ElementTree as et

def main():
	print "XML Parse Script"
	tree = et.parse("allagents.xml")

# these two iterations do the same thing
#	for elem in tree.getiterator("String"):
#		print elem.text.encode('utf-8')
	for elem in tree.getiterator("user-agent"):
		print et.tostring(elem)
		stringelem = elem.find("String")
		print stringelem.text.encode('utf-8')
			
	return 0
if __name__ == "__main__":
	main()


