# RE-Invest 
A web based application for real estate investors.

## Introduction
The goal of this project was to develop my programming skill set by building an application that interested me. 
A user can calculate real estate metrics such as capitalization rates by entering assumptions such as purchase price, mortgage info, and monthly rent. 

The backend was built using Python's Flask framework and a MYSQL database hosted on AWS Relational Database Service. 
Pages are built in HTML with CSS styling and Javascript to improve responsiveness. 
The application was deployed on a Free Tier instance of Amazon Web Services Elastic Beanstalk. 

## Lessons Learned
This project was crucial in my development as a software engineer. 

I believe the biggest skill I gained from this project was resourcefulness, self sufficiency, and persistence. 
Besides the Bootstrap CSS template, this entire application was built from scratch. 
It was not a tutorial I followed from start to finish. 
Instead, I was forced to break down large problems into smaller chunks, solve the smaller chunks and put it all back together.
I learned how frustrating bugs can be, wanting to quit midway, but pushing through a successful feature implementation.
I learned how to set deadlines so the project would not drag on indefinitely and use project management software such as Trello to remember everything.  

The time spent on this project was nearly 2 months (52 days to be exact). 
I spent a few hours everyday after work and 2-8 hours on the weekend. 
Estimated total time spent was 160 hours and every single hour was worth it. 

With this experience, I am confident that I can learn new technologies for any task.

A few lessons learned are below:
- Flask framework 
- Amazon Web Services  
- Version control
- Object Oriented Programming
- MVC design pattern 
- HTTPS
- Database
- HTML/CSS
- Javascript
- Testing/Debugging


## Features 
1. Property Analyzer
    - Creates a report with metrics such as Net Operating Income, Cash on Cash Return, etc. 

2. Mortgage Calculator
    - Uses Javascript and AJAX to asynchronously submit data 
   
3. User Registration
    - A registered user will be able to save their reports to a My Properties tab.
    - They will be able to edit, delete, or share the report.





###



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
