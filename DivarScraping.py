from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import html5lib
import re
import time

options = Options()
options.add_argument('--headless')
options.set_preference('permissions.default.image', 2)
options.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)


# get_ads_links() function returns a list of links approximately as many as desired
def get_ads_links(my_url, number, html_class: str):
    web_driver = webdriver.Firefox(options=options)
    web_driver.get(my_url)
    links = []
    timeout = 2
    number = int(number / 10)
    for i in range(number):
        # Once scroll returns bs4 parsers the page_source
        soup = BeautifulSoup(web_driver.page_source, 'html5lib')
        # Them we close the driver as soup_a is storing the page source
        ads = soup.find_all('a', class_=html_class, href=True)
        # Empty array to store the links
        for ad in ads:
            ad_url = 'https://divar.ir' + str(ad['href'])
            links.append(ad_url)
        # This starts the scrolling by passing the driver and a timeout
        web_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(timeout)
    web_driver.close()
    return links


# car_information() function returns a dictionary containing of car information
def car_information(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html5lib')
    car_model = soup.find('a', class_="kt-unexpandable-row__action kt-text-truncate", href=True)
    if car_model:
        car = re.findall(r"/car/(.+)/(.+)/", car_model['href'])
        if car:
            brand, model = car[0]
            similar_link = 'https://divar.ir/s/tehran/car/' + str(brand + '/' + model)
            print(similar_link, '\n', brand, model)
        else:
            car = re.findall(r"/car/(.+)/(.+)", car_model['href'])
            if car:
                brand, model = car[0]
                similar_link = 'https://divar.ir/s/tehran/car/' + str(brand + '/' + model)
                print(similar_link, '\n', brand, model)
            else:
                car = re.findall(r"/car/(.+)", car_model['href'])
                if car:
                    brand = car[0]
                    model = None
                    similar_link = 'https://divar.ir/s/tehran/car/' + str(brand + '/' + model)
                    print(similar_link, '\n', brand, model)


# Scraping car information from https://divar.ir/
site_url = "https://divar.ir/s/tehran/auto?non-negotiable=true&exchange=exclude-exchanges"
urls = get_ads_links(site_url, 100, "kt-post-card kt-post-card--outlined")
for url in urls:
    car_information(url)
