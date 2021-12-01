import requests
import html5lib
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import re

options = Options()
options.add_argument('--headless')
options.set_preference('permissions.default.image', 2)
options.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)


# car_ad_links() function returns a list of links approximately as many as desired
def car_ad_links(number):
    ad_links = []
    timeout = 1
    number = int(number / 10)
    web_driver = webdriver.Firefox(options=options)
    web_driver.get("https://divar.ir/s/tehran/auto")
    for i in range(number):
        # Once scroll returns bs4 parsers the page_source
        soup = BeautifulSoup(web_driver.page_source, 'html5lib')
        # Them we close the driver as soup_a is storing the page source
        ads = soup.find_all('a', class_="kt-post-card kt-post-card--outlined", href=True)
        # Empty array to store the links
        for ad in ads:
            ad_url = 'https://divar.ir' + str(ad['href'])
            ad_links.append(ad_url)
        # This starts the scrolling by passing the driver and a timeout
        web_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(timeout)
    web_driver.close()
    return ad_links


# car_data() function returns a dictionary containing of car data for using in database
def car_data(link):
    global brand, model
    response = requests.get(link)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html5lib')
        # brand and model values is extracted from car ad URL
        car_model = soup.find_all('a', class_="kt-unexpandable-row__action kt-text-truncate", href=True)
        if car_model:
            car = re.findall(r"/car/(.+)/(.+)/", car_model[-1]['href'])
            if car:
                brand, model = car[0]
            else:
                car = re.findall(r"/car/(.+)/(.+)", car_model[-1]['href'])
                if car:
                    brand, model = car[0]
                else:
                    car = re.findall(r"/car/(.+)", car_model[-1]['href'])
                    if car:
                        brand = car[0]
                        model = ''
            # This condition is used to ensuring for brand variables values
            if brand == 'dealers':
                return
            # car_WYC variable is a list containing worked, year and color features
            car_WYC = soup.find_all('span', class_="kt-group-row-item__value")
            worked = car_WYC[0].string
            if '٫' in worked:
                worked = car_WYC[0].string.replace('٫', '')
            year = car_WYC[1].string
            if 'قبل از ' in year:
                year = car_WYC[1].string.replace('قبل از ', '')
            worked, year, color = int(worked), int(year), car_WYC[2].string
            # Creating a dictionary for other car features
            car_info_title = soup.find_all('p', class_="kt-base-row__title kt-unexpandable-row__title")
            car_info_values = soup.find_all('p', class_="kt-unexpandable-row__value")
            other_info = {}
            for i in range(len(car_info_values)):
                other_info[car_info_title[i + 1].string] = car_info_values[i].string
            price = car_info_values[-1].string
            # Only values for the price are stored in database that are integer
            if price in {'غیرقابل نمایش', 'برای معاوضه', 'توافقی'}:
                return
            else:
                if '٬' in price:
                    price = price.replace('٬', '')
                if ' تومان' in price:
                    price = price.replace(' تومان', '')
                price = int(price)
            other_info.setdefault('وضعیت موتور')
            engine_status = other_info['وضعیت موتور']
            other_info.setdefault('وضعیت شاسی‌ها')
            chassis_status = other_info['وضعیت شاسی‌ها']
            other_info.setdefault('وضعیت بدنه')
            body_status = other_info['وضعیت بدنه']
            other_info.setdefault('مهلت بیمهٔ شخص ثالث')
            insurance_deadline = other_info['مهلت بیمهٔ شخص ثالث']
            if insurance_deadline:
                if ' ماه' in insurance_deadline:
                    insurance_deadline = int(insurance_deadline.replace(' ماه', ''))
            car_info = {'brand': brand, 'model': model, 'worked': worked, 'year': year, 'color': color,
                        'price': price, 'engine_status': engine_status, 'chassis_status': chassis_status,
                        'body_status': body_status, 'insurance_deadline': insurance_deadline}
            return car_info
        else:
            return
    else:
        return


# The similar_ads() function returns a list of similar links
def similar_ads(link):
    global brand, model
    response = requests.get(link)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html5lib')
        car_model = soup.find_all('a', class_="kt-unexpandable-row__action kt-text-truncate", href=True)
        if car_model:
            car = re.findall(r"/car/(.+)/(.+)/", car_model[-1]['href'])
            if car:
                brand, model = car[0]
            else:
                car = re.findall(r"/car/(.+)/(.+)", car_model[-1]['href'])
                if car:
                    brand, model = car[0]
                else:
                    car = re.findall(r"/car/(.+)", car_model[-1]['href'])
                    if car:
                        brand = car[0]
                        model = ''
                    else:
                        return
            ads_link = 'https://divar.ir/s/tehran/car/' + str(brand + '/' + model)
            if requests.get(ads_link).ok:
                return ads_link


# car_information() function returns a dictionary containing of car information for show to user
def car_information(link):
    response = requests.get(link)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html5lib')
        car_model = soup.find_all('a', class_="kt-unexpandable-row__action kt-text-truncate", href=True)
        if car_model:
            dealer = None
            if len(car_model) == 2:
                dealer = car_model[0].string
            model_and_tip = car_model[-1].string
            car_WYC = soup.find_all('span', class_="kt-group-row-item__value")
            worked = car_WYC[0].string
            if '٫' in worked:
                worked = car_WYC[0].string.replace('٫', '')
            year = car_WYC[1].string
            color = car_WYC[2].string
            car_info_title = soup.find_all('p', class_="kt-base-row__title kt-unexpandable-row__title")
            car_info_values = soup.find_all('p', class_="kt-unexpandable-row__value")
            other_info = {}
            if len(car_model) == 1:
                for i in range(len(car_info_values)):
                    other_info[car_info_title[i + 1].string] = car_info_values[i].string
            elif len(car_model) == 2:
                for i in range(len(car_info_values)):
                    other_info[car_info_title[i + 2].string] = car_info_values[i].string
            price = car_info_values[-1].string
            other_info.setdefault('وضعیت موتور')
            engine_status = other_info['وضعیت موتور']
            other_info.setdefault('وضعیت شاسی‌ها')
            chassis_status = other_info['وضعیت شاسی‌ها']
            other_info.setdefault('وضعیت بدنه')
            body_status = other_info['وضعیت بدنه']
            other_info.setdefault('مهلت بیمهٔ شخص ثالث')
            insurance_deadline = other_info['مهلت بیمهٔ شخص ثالث']
            car_info = {'مدل': model_and_tip, 'کارکرد': worked, 'سال تولید': year, 'رنگ': color,
                        'قیمت': price, 'وضعیت موتور': engine_status, 'وضعیت شاسی‌ها': chassis_status,
                        'وضعیت بدنه': body_status, 'مهلت بیمهٔ شخص ثالث': insurance_deadline}
            if dealer:
                car_info.setdefault('نمایشگاه', dealer)
            return car_info
        else:
            return
    else:
        return
