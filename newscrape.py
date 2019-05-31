import os
from selenium import webdriver
from bs4 import BeautifulSoup
from realtoranalysis.oldscrape import listing_meta
from realtoranalysis.scrape import listing_json


def try_both(url):
    # specify path to chrome driver

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")
    driver = webdriver.Chrome(executable_path = DRIVER_BIN)

    # run specified URL in chrome through selenium webdriver
    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')   # soup variable contains the entire page source

    if 'application/json' in soup:
        script_text = soup.find('script', {'type': 'application/json'}).get_text()
        data = json.loads(script_text)  # a dictionary!

        property_detail = data['props']['pageProps']['property']

        list_price = property_detail['list_price']
        bedrooms = property_detail['details'][0]
        bathrooms = property_detail['details'][3]
        schools = property_detail['details'][7]
        sqft = property_detail['details'][11]
        testss = property_detail['description']

        print(list_price)
        print(bedrooms)
        print(bathrooms)
        print(schools)
        print(sqft)
        print(testss)

    else:
        container = soup.find('div', {'class': 'listing-header-main'})

        if len(container) > 0 or container is not None:
            price = container.find('span', {'itemprop': 'price'}).text
            bed = container.find('li', {'data-label': 'property-meta-beds'}).text
            bath = container.find('li', {'data-label': 'property-meta-bath'}).text
            sqft = container.find('li', {'data-label': 'property-meta-sqft'}).text
        else:
            print('Check code')

        # clean scraped variables
        list_price = price.split()[0].split('$')[1].replace(',', '')
        bedrooms = bed.split()[0]
        bathrooms = bath.split()[0]
        sqft = sqft.split()[0].replace(',', '')

        print(list_price)
        print(bedrooms)
        print(bathrooms)
        print(sqft)

tryboth(r'https://www.realtor.com/realestateandhomes-detail/104-Aruba-Ct_Austin_TX_78734_M75037-62575?view=qv')