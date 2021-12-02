from DivarScraping import *
import Database
from Database import insert_data
import os, stat


def save_data(n):
    urls = car_ad_links(n)
    for url in urls:
        data = car_data(url)
        if data and data != "Error!":
            insert_data(data)


def latest_ads(n):
    counter = 1
    num = n * 3
    file = open("latest-car-ads.txt", 'a')
    urls = car_ad_links(num)
    for url in urls:
        if counter <= n:
            car_info = car_information(url)
            if car_info:
                for key, value in car_info.items():
                    file.write('{0:>15s}:  {1:>20s}\t'.format(key, value))
                counter += 1
                file.write('\n')
    file.close()


latest_ads(30)
