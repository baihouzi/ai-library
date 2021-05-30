import pymysql

from const import *

connection = pymysql.connect(host=MYSQL_HOST,
                             port=MYSQL_PORT,
                             user=MYSQL_USER,
                             password=MYSQL_PASSWORD,
                             db=MYSQL_DB,
                             charset='utf8')

cursor = connection.cursor()

books_sql = '''
CREATE TABLE books (
    id int PRIMARY KEY AUTO_INCREMENT,
    title varchar(50) NOT NULL,
    author varchar(50) NOT NULL,
    serial varchar(50) NOT NULL,
    intro varchar(240),
    borrower int DEFAULT -1, 
    create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8
'''
try:
    ret = cursor.execute(books_sql)
except Exception as err:
    print(err)

faces_sql = '''
CREATE TABLE faces (
    id int PRIMARY KEY AUTO_INCREMENT,
    name varchar(10) NOT NULL,
    create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8
'''
try:
    ret = cursor.execute(faces_sql)
except Exception as err:
    print(err)

connection.close()
