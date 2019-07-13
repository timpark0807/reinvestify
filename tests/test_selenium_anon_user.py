import os
import time
from selenium import webdriver


##############################################################################
# Setup
##############################################################################

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")
driver = webdriver.Chrome(executable_path=DRIVER_BIN)

url = 'http://127.0.0.1:5000/'
driver.get(url)

##############################################################################
# Click side bar navigation menu
##############################################################################

driver.find_element_by_id("properties").click()
driver.find_element_by_id("analyze").click()
driver.find_element_by_id("calculator").click()
driver.find_element_by_id("about").click()

##############################################################################
# Test that the analyze form works
##############################################################################

# Tab 1
driver.find_element_by_id("analyze").click()
driver.find_element_by_id("title").send_keys('selenium report test')
driver.find_element_by_name("street").send_keys('21 West Selenium')
driver.find_element_by_name("city").send_keys('Selenium')
driver.find_element_by_name("state").send_keys('SE')
driver.find_element_by_name("zipcode").send_keys('12345')
driver.find_element_by_id("next-1").click()

# Tab 2
driver.find_element_by_name("year").send_keys('2019')
driver.find_element_by_name("bed").send_keys('4')
driver.find_element_by_name("bath").send_keys('2')
driver.find_element_by_name("sqft").send_keys('4500')
driver.find_element_by_id("next-2").click()

# Tab 3
driver.find_element_by_id("next-3").click()

# Tab 4
driver.find_element_by_id("final_submit").click()

##############################################################################
# Delete
##############################################################################

time.sleep(3)

# Delete the report
driver.find_element_by_id("delete").click()
time.sleep(3)
driver.find_element_by_id("delete_confirm").click()


##############################################################################
# Exit
##############################################################################
time.sleep(3)
driver.quit()