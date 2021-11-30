import mysql.connector


# Connect to MySQL
my_db = mysql.connector.connect(host='127.0.0.1', user='root', password='javad76mi')
my_cursor = my_db.cursor()
my_cursor.execute("DROP DATABASE IF EXISTS CarInfo;")

# Create database and table
my_cursor.execute("CREATE DATABASE IF NOT EXISTS CarInfo;")
my_db = mysql.connector.connect(host='127.0.0.1', user='root', password='javad76mi', database='CarInfo')
my_cursor = my_db.cursor()
my_cursor.execute("""CREATE TABLE IF NOT EXISTS CarFeatures(brand VARCHAR(25), model VARCHAR(20), year INT(20),
     worked INT(255), price BIGINT(255), color VARCHAR(20), engine_status VARCHAR(20), chassis_status VARCHAR(25),
     body_status VARCHAR(25), insurance_deadline INT(20));""")
