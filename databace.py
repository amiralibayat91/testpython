import mysql.connector

cnx = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1',
                              database='pipi')

name = 'hasan'
mmm = 'm'
age = 12


cursor = cnx.cursor()
cursor.execute('INSERT INTO pipi VALUES (\'%s\', \'%s\', %i)' % (name, mmm, age))
cnx.commit()

cnx.close()