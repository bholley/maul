class uaobject:
	def __init__(self):
		self.uaString = str()
		self.data = dict()
	def getstring(self):
		r = self.uaString + '\n'
		for k, v in self.data.items():
			r = r + k + ': ' + v + '\n'	
		return r
	def __add__(self,String):  # define string addition 
		r = self.getstring() + String
		return r
	def __str__(self):
		r = self.getstring()
		return r
	def readEntry(fh,self):
		self.uaString, self.data = readEntry(fh)

def readEntry(fh): # fh is a filehandle

  	# Skip blank lines until we find something
	uaString = "\n"
  	while re.match("^\s*$", uaString):
   	# Python returns "\n" for blank lines, "" for EOF
		if (uaString == ""):
			return "EOF"
		uaString = fh.readline()
	uaString = uaString.strip()

  # Get the properties
	props = dict()
	prop = fh.readline()
	while not re.match("^[\s\n]*$", prop): # while not an empty line

    		# Split the string
		category, sep, value = prop.partition(':')
		category = category.strip()
		value = value.strip()

			# Validate
		if not sep:
			raise RuntimeError("Bad Input line: " + prop)
		if category not in categories:
			raise RuntimeError("Unknown category: " + category)
		if category in props:
			raise RuntimeError("Duplicate property " + category + " in UA String: " + uaString)

   		# Store the property
		props[category] = value

		# Read another line
		prop = fh.readline()

	return (uaString, props)
