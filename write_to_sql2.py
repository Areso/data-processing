import MySQLdb
import streets

import MySQLdb
filename = 'config.txt'
lineList = list()
with open(filename) as f:
  for line in f:
    lineList.append(line)


mydbhost = lineList[0]
mydbhost = mydbhost.rstrip()

mydbname = lineList[1]
mydbname = mydbname.rstrip()

mydbuser = lineList[2]
mydbuser = mydbuser.rstrip()

mydbpass = lineList[3]
mydbpass = mydbpass.rstrip()
db = MySQLdb.connect(host=mydbhost,
                          database=mydbname,
                          user=mydbuser,
                          password=mydbpass)
cur = db.cursor()
sql_insert_query = """ INSERT INTO `test`
                       (`id`, `name`) VALUES (1,'test')"""
cur.execute(sql_insert_query)
