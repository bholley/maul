import sys,os, sqlite3, re
sys.path.append('../src/')
from Common import categories




# need to load 2 DB's and delete entries from second one in first one
db1 = 'maul.db'
db2 = 'nastydb'
db1copy = db1 + '.excl'
# make a copy
cmd = 'cp ' + db1+ ' '+ db1copy
os.system(cmd)

conn1 = sqlite3.connect(db1copy)
conn1.text_factory = str
c1 = conn1.cursor()

conn2 = sqlite3.connect(db2)
conn2.text_factory = str
c2 = conn2.cursor()

# are tokens in db1?


# get all token strings from db2
c2.execute('select Tokens from data')
tokenlist = []
for item in c2:
    tokenstr = item[0]
    tokenstr = '"' + tokenstr + '"'
    tokenlist.append(tokenstr)
# remove from db1
#    c1.execute('delete from data where Tokens = '+tokenstr)


# are strings in DB1?
print "Looking up uaString for tokens"
for tokenstr in tokenlist:
    c1.execute('select uaString from data where Tokens = ' +tokenstr)
    for x in c1:
        print x[0]
    c1.execute('delete from data where Tokens = ' + tokenstr)


# make sure gone
print "Checking to make sure gone"
for tokenstr in tokenlist:
    c1.execute('select uaString from data where Tokens = ' +tokenstr)
    for x in c1:
        print x[0]


# commit DB;
conn1.commit()
c1.close()
c2.close()

