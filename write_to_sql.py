import MySQLdb

#import mysql.connector
#from mysql.connector import Error
#from mysql.connector import errorcode
import streets


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
#import mysql.connector
#from mysql.connector import Error
#from mysql.connector import errorcode
try:
   connection = mysql.connector.connect(host=mydbhost,
                             database=mydbname,
                             user=mydbuser,
                             password=mydbpass)
   sql_insert_query = """ INSERT INTO `test`
                          (`id`, `name`) VALUES (1,'test')"""
   cursor = connection.cursor()
   result  = cursor.execute(sql_insert_query)
   connection.commit()
   print ("Record inserted successfully into python_users table")
except mysql.connector.Error as error :
    connection.rollback() #rollback if any exception occured
    print("Failed inserting record into python_users table {}".format(error))
finally:
    #closing database connection.
    if(connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")