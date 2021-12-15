import mysql.connector
from DivarScraping import *
import pandas as pd


# With this function we can create database and table and connect to it
def database_settings():
    # Connecting to localhost
    my_db = mysql.connector.connect(host='127.0.0.1', user='root', password='YOUR_ROOT_PASSWORD')
    my_cursor = my_db.cursor()
    # Creating database
    my_cursor.execute("CREATE DATABASE IF NOT EXISTS CarInfo;")
    my_db = mysql.connector.connect(host='127.0.0.1', user='root', password='YOUR_ROOT_PASSWORD', database='CarInfo')
    my_cursor = my_db.cursor()
    # Creating table with its features
    my_cursor.execute("""CREATE TABLE IF NOT EXISTS CarFeatures(ID VARCHAR(255), brand VARCHAR(255), model VARCHAR(255),
        year INT(255), worked INT(255), price BIGINT(255), color VARCHAR(255), engine_status VARCHAR(255),
        chassis_status VARCHAR(255), body_status VARCHAR(255), insurance_deadline INT(255), PRIMARY KEY (ID));""")


# This function is defined for saving a row to database with input dicrionary
def insert_data(data_dic):
    values = tuple(data_dic.values())
    my_db = mysql.connector.connect(host='127.0.0.1', user='root', password='YOUR_ROOT_PASSWORD', database='CarInfo')
    my_cursor = my_db.cursor()
    # We use this condition to prevent duplicate data insert
    dataframe = pd.read_sql("SELECT ID FROM CarFeatures WHERE ID = '{}';".format(values[0]), my_db)
    if dataframe.empty:
        # Insert row to database
        my_cursor.execute("INSERT INTO CarFeatures VALUES {};".format(values))
        # Applying changes to database
        my_db.commit()


def save_latest_ads(n):
    number = int(n * 1.5)
    urls = car_ad_links(number, "https://divar.ir/s/tehran/auto")
    for url in urls:
        data = car_data(url)
        if data != "Error!":
            insert_data(data)
    print("Done!")


def save_desired_ads(brand, model, n):
    ads_url = 'https://divar.ir/s/tehran/car/' + brand + '/' + model
    if requests.get(ads_url).ok:
        urls = car_ad_links(n, ads_url)
        for url in urls:
            data = car_data(url)
            if data != "Error!":
                insert_data(data)
        print("Done!")
    else:
        return "Error!"


# It gives to us a csv file of data
def export_data():
    my_db = mysql.connector.connect(host='127.0.0.1', user='root', password='YOUR_ROOT_PASSWORD', database='CarInfo')
    dataframe = pd.read_sql("SELECT * FROM CarFeatures;", my_db)
    dataframe.to_csv("Saved_Data/Cars-data.csv")
