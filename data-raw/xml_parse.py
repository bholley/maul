import elementtree.ElementTree as et

def main():
	print "XML Parse Script"
	tree = et.parse("allagents.xml")

# these two iterations do the same thing
#	for elem in tree.getiterator("String"):
#		print elem.text.encode('utf-8')
	for elem in tree.getiterator("user-agent"):
		stringelem = elem.find("String")
		print stringelem.text.encode('utf-8')
		typeelem = elem.find("Type")
		if typeelem.text == "R":
			print "Robot"
		elif typeelem.text == "B":
			print "Browser"
		elif typeelem.text == "C":
			print "Validator"
	return 0
if __name__ == "__main__":
	main()


