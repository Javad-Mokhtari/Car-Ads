from DivarScraping import *


def main():
    # Scraping car information from https://divar.ir/
    urls = car_ad_links(200)
    for url in urls:
        if car_information(url):
            print(car_information(url))


if __name__ == '__main__':
    main()
