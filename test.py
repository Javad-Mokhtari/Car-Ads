def scroll(webdriver, number, timeout):
    scroll_pause_time = timeout
    # Get scroll height
    last_height = webdriver.execute_script("return document.body.scrollHeight")
    for i in range(number):
        # Scroll down to bottom
        webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(scroll_pause_time)


"""        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If heights are the same it will exit the function
            break
        last_height = new_height"""


options = Options()
options.add_argument('--headless')
options.set_preference('permissions.default.image', 2)
options.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)


def all_links(url):
    # Setup the driver. This one uses firefox with some options and a path to the geckodriver
    web_driver = webdriver.Firefox(options=options)
    # implicitly_wait tells the driver to wait before throwing an exception
    web_driver.implicitly_wait(30)
    # driver.get(url) opens the page
    web_driver.get(url)
    # This starts the scrolling by passing the driver and a timeout
    scroll(web_driver, 5)
    # Once scroll returns bs4 parsers the page_source
    soup_a = BeautifulSoup(web_driver.page_source, 'html')
    # Them we close the driver as soup_a is storing the page source
    web_driver.close()

    # Empty array to store the links
    links = []

    # Looping through all the a elements in the page source
    for link in soup_a.find_all('a'):
        # link.get('href') gets the href/url out of the a element
        links.append(link.get('href'))

    return links


driver = webdriver.Firefox(options=options)
driver.get('https://www.google.com/doodles')

print('Title: "{}"'.format(driver.title))
driver.quit()

print(all_links("https://divar.ir/s/tehran/auto?non-negotiable=true&exchange=exclude-exchanges"))
