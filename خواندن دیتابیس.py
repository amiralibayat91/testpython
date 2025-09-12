import mysql.connector

cnx = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1',
                              database='pipi')

cursor=cnx.cursor()


query = 'SELECT * FROM pipi;'
cursor.execute(query)

for (name, sex, age) in cursor:
    print ('%s is a %s and the age is %i' % (name, sex, age))

cnx.close()