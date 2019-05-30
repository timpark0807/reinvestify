You will need the following packages:
-BeautifulSoup
-Requests

Download the latest version of ChromeDriver

scrape.py looks for the json output found in the page source 
-this contains much more information than the method used in oldscrape.py


oldscrape.py attempted to look for each individual tag. the problem with this was that dynamically generated javascript pages would change the tags for variables for different cities. I'm not completely sure on the reasoning why, but it would create an error after i set up all the proper tags for price, bed, bath for santa barbara. Running a cincinati house would create an error as the tag for bed changed from 'property-meta-beds' to 'jxa1234314' (a random combination of variables and characters). 