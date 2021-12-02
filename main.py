from DivarScraping import *
import SaveData
from SaveData import insert_data


def main():
    # Scraping car information from https://divar.ir/
    urls = car_ad_links(200)
    for url in urls:
        data = car_data(url)
        if data:
            print(data)
            insert_data(data)


if __name__ == '__main__':
    main()
