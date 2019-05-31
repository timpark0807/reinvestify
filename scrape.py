import os
import json
from selenium import webdriver
from bs4 import BeautifulSoup


def listing_json(url):
    """Scrapes Realtor.com home listings and returns content.
        Grabs the json data that contains so much more information than the old way I was doing with selenium

       Parameters
       ----------
       url : str

       Returns
       ----------
       - Street Address
       - Zip Code
       - Asking Price
       - Bed/Bath
       - Square Foot
       - Picture
       """

    # specify path to chrome driver
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")
    driver = webdriver.Chrome(executable_path = DRIVER_BIN)

    # run specified URL in chrome through selenium webdriver
    driver.get(url)

    # get html of url so we can parse the information
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')   # soup variable contains the entire page source

    script_text = soup.find('script', {'type':'application/json'}).get_text()
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

# listingjson(r'https://www.realtor.com/realestateandhomes-detail/3211-Glenmore-Ave_Cincinnati_OH_45211_M33941-68330?view=qv')