from DivarScraping import *
from Database import *
import Database
import re


def save_latest_ads(n):
    number = int(n * 1.5)
    urls = car_ad_links(number, "https://divar.ir/s/tehran/auto")
    for url in urls:
        data = car_data(url)
        if data != "Error!":
            insert_data(data)
    print("Done!")


def save_favorite_ads(brand, model, n):
    ads_url = 'https://divar.ir/s/tehran/car/' + brand + '/' + model
    if requests.get(ads_url).ok:
        urls = car_ad_links(n, ads_link)
        for url in urls:
            data = car_data(url)
            if data != "Error!":
                insert_data(data)
        print("Done!")
    else:
        return "Error!"
