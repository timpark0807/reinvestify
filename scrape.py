import os
import json
from selenium import webdriver
from bs4 import BeautifulSoup


def listingjson(url):
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
    print(json.dumps(data, indent=4))


listingjson(r'https://www.realtor.com/realestateandhomes-detail/3409-Boudinot-Ave_Cincinnati_OH_45211_M33765-41540?view=qv')