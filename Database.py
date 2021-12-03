import mysql.connector
from DivarScraping import car_data
import pandas as pd


# Connect to MySQL
my_db = mysql.connector.connect(host='127.0.0.1', user='root', password='javad76mi')
my_cursor = my_db.cursor()
# Create database and table
my_cursor.execute("CREATE DATABASE IF NOT EXISTS CarInfo;")
my_db = mysql.connector.connect(host='127.0.0.1', user='root', password='javad76mi', database='CarInfo')
my_cursor = my_db.cursor()
my_cursor.execute("""CREATE TABLE IF NOT EXISTS CarFeatures(ID VARCHAR(255), brand VARCHAR(255), model VARCHAR(255),
                     year INT(255), worked INT(255), price BIGINT(255), color VARCHAR(255), engine_status VARCHAR(255),
                     chassis_status VARCHAR(255), body_status VARCHAR(255), insurance_deadline INT(255));""")


def insert_data(data_dic):
    values = []
    for column in data_dic.keys():
        values.append(data_dic[column])
    my_cursor.execute("INSERT INTO CarFeatures VALUES {};".format(tuple(values)))
    my_db.commit()


def export_data():
    dataframe = pd.read_sql("SELECT * FROM CarFeatures;", my_db)
    dataframe.to_csv("Data/Cars-data.csv")


def clean_duplicated():
    pass
