import sqlite3

#connect to the database
conection = sqlite3.connect('student.db')

#create a cursor object
cursor = conection.cursor()

#create a table
table_info = """
Create table STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25), 
SECTION VARCHAR(25));
"""

cursor.execute(table_info)

#Insert more records

cursor.execute(''' INSERT INTO STUDENT VALUES('John', '10th', 'A') ''')
cursor.execute(''' INSERT INTO STUDENT VALUES('Jane', '10th', 'B') ''')
cursor.execute(''' INSERT INTO STUDENT VALUES('Jim', '10th', 'C') ''')

print("Table created successfully")
data = cursor.execute(''' SELECT * FROM STUDENT ''')
for row in data:
    print(row)

#close the connection
conection.close()