import os
import pymysql.connections

MYSQL_HOST = '10.192.63.114'
#MYSQL_DB = 'scada'
MYSQL_DB = 'catalina_hmi'
MYSQL_USER = 'gRPC'
MYSQL_PASS = 'test'

conn = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASS,
    db=MYSQL_DB,
    port=3306,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)