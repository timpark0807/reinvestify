import os
from selenium import webdriver
from bs4 import BeautifulSoup


def listing_meta(url):

    """Scrapes Realtor.com home listings and returns content.

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
    # data = requests.get(url).text

    # specify path to chrome driver
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")
    driver = webdriver.Chrome(executable_path = DRIVER_BIN)

    # run specified URL in chrome through selenium webdriver
    driver.get(url)

    # get html of url so we can parse the information
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')   # soup variable contains the entire page source

    # this container isolates the container that contains all the property information we are looking for
    container = soup.find('div', {'class':'listing-header-main'})

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


    return list_price, bedrooms, bathrooms, sqft