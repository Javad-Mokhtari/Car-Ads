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


# cars_information() function returns a 2D list from cars information
def cars_information(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html5lib')
    # car = soup.find('p', class_="kt-base-row__title kt-unexpandable-row__title", text='برند و تیپ')
    car = soup.find_all('div', class_="kt-unexpandable-row__action kt-text-truncate", href=True)
    # model_link = list(filter(lambda a: 'برند و تیپ' in car.find_all('p', class_="kt-base-row__title "
    #                                                                            "kt-unexpandable-row__title"), car))
    # print(model_link)
    print(car)

"""    if car is not None:
        car = re.findall(r"/car/(.+)/*(.*)", car['href'])
    if car is not None:
        brand, model = car[0]
        print(brand, model)"""

# Scraping car information from https://divar.ir/
site_url = "https://divar.ir/s/tehran/auto?non-negotiable=true&exchange=exclude-exchanges"
urls = get_ads_links(site_url, 100, "kt-post-card kt-post-card--outlined")
for url in urls:
    cars_information(url)
