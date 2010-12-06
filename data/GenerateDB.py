import sys
import os
import sqlite3
import re
sys.path.append('../src/')
from Common import categories

"""Helper Routines"""

# Creates the table
def createTable(c):
  createString = 'create table data ("uaString" text NOT NULL'
  for category in categories:
    createString = createString + ', '
    createString = createString + '"' + category + '"' + ' text'
  createString = createString + ')'
  c.execute(createString)

def readEntry(fh):

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
  while not re.match("^[\s\n]*$", prop):

    # Split the string
    category, sep, value = prop.partition(':')
    category = category.strip().rstrip()
    value = value.strip().rstrip()

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

def readFileDB(filename, c):
  file = open(filename, 'r')

  # Loop until we hit eof
  entryCount = 0
  while True:

    # Read an entry. This either returns a valid tuple or "EOF"
    tuple = readEntry(file)
    if (tuple == "EOF"):
      break

    # Insert the UA string into the database
    # FIXME
    keyString = '"uaString"'  # start keystring as  just a uaString
    vals = [tuple[0]]   # start vals as just the uaString itself
    questionMarks = '?'
    for key, val in tuple[1].items(): #add in other data
      keyString = keyString + ', "' + key + '"'
      vals.append(val)
      questionMarks = questionMarks + ', ?'
    insertString = 'insert into data (' + keyString + ') VALUES(' + questionMarks + ')'
    c.execute(insertString, vals)

    # Statistics
    entryCount = entryCount + 1

  print "Read %d entries from %s" % (entryCount, filename)

# Print usage
def printUsage():
  print "Usage: " + sys.argv[0] + " DBFILE DATAFILE1 DATAFILE2 DATAFILE3 ..."


"""Main Program"""

# Check that we have the right number of arguments
if len(sys.argv) < 3:
  printUsage()
  sys.exit(2)

# Separate args
dbfile = sys.argv[1]
datafiles = sys.argv[2:]

# Remove anything that was there before
try:
  os.remove(dbfile)
except OSError:
  None

# Open DB connection
conn = sqlite3.connect(sys.argv[1])

# User-Agent strings should always be ascii (I think...)
conn.text_factory = str

# Create our cursor (db handle)
c = conn.cursor()

# Create a table
createTable(c)

# Read in each input file
for datafile in datafiles: readFileDB(datafile, c)

# Clean up
conn.commit()
c.close()


