# Real Estate Investing Portal 
## RE-Invest 

RE-Invest is a web based application for real estate investors. My goal was to learn more about programming by creating an application that interested me. 

Features:
1. Property Analyzer
2. Mortgage Calculator

Property Analyzer takes inputs from the users and creates a report with metrics such as Net Operating Income, Cash on Cash Return, etc. 







You will need the following packages:
-BeautifulSoup
-Requests

Download the latest version of ChromeDriver

scrape.py looks for the json output found in the page source 
-this contains much more information than the method used in oldscrape.py

oldscrape looks for the information through html tags

Some locations will require json method while others require html tag method. Therefore, I built an if statement to check if "application/json" was found within the page source of the scraped file. If it was, json method would trigger. If it wasn't the html tag method would trigger.

I wrote a test for listing_json. Will need to write a test for listing_meta.

TODO:
1. Create an Excel workbook where I can place list price and other relevant information on.
2. Create cash flow calculations on the Excel workbook
3. Create a Flask webform that will take the URL and rent price
4. Host the app on AWS 
5. 

oldscrape.py attempted to look for each individual tag. the problem with this was that dynamically generated javascript pages would change the tags for variables for different cities. I'm not completely sure on the reasoning why, but it would create an error after i set up all the proper tags for price, bed, bath for santa barbara. Running a cincinati house would create an error as the tag for bed changed from 'property-meta-beds' to 'jxa1234314' (a random combination of variables and characters). 
