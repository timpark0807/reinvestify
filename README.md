# reinvestify.com
A web application that analyzes the profitability of real estate investments. 

## Introduction
The goal of this project was to showcase my programming skill set. 
I chose this niche due to my curiousity and interest in real estate investing. 
The total time spent on this project was ~2.5 months. 

The backend of reinvestify was built using Python's Flask framework. 
This is connected to a MYSQL database instance that is hosted on the AWS Relational Database Service. 
The front end pages were built in HTML with CSS styling and some Javascript to improve responsiveness. 
The entire application was deployed on a Free Tier instance of AWS using Elastic Beanstalk. 

The main function of reinvestify is generating reports on real estate investments. 
The application captures user inputs such as purchase price, mortgage rates, rental incomes, and operating expenses and calculates metrics such as capitalization rates, cash on cash return, and monthly cash flow. 

An example of a report is below.

[![Screen-Shot-2019-12-31-at-4-06-13-PM.png](https://i.postimg.cc/y6fmW40T/Screen-Shot-2019-12-31-at-4-06-13-PM.png)](https://postimg.cc/DmXJYNjW)

## Features 
#### Property Analyzer
The user begins by entering property and purchase assumptions on a 4 step form. 
Different sections of the form are loaded on the same page using Javascript.

On form submission, numbers are preprocessed in a Calculate object that generates metrics such as cap rates, cash on cash, noi, etc.
A POST request containing the preprocessed calculations and form text inputs (street address, property type, bed/bath/sqft, etc.) is sent to the MYSQL database where entry is created with a unique post ID key. 

After the POST request is completed, the user is redirected to a view route that has the unique post id key at the end of the url. 
This view route queries the database using the specified post_id key as the WHERE operator in a SQL statement. 
The query results are packaged into a hashtable and returned to the front end HTML template. 
Now the front end HTML template has access the preprocessed calculations and form text inputs previously submitted via POST request.

![Imgur Image](https://i.imgur.com/GGIkdKm.png)

#### Mortgage Calculator
The mortgage calculator calculates the monthly mortgage payment based on a user's input of purchase price, down payment, loan term, and interest rate. 
Utilizes Javascript and AJAX to asynchronously submit data.

![Imgur Image](https://i.imgur.com/mSnUl7.png)
 
#### User Registration
Users can choose to register in order to save generated reports to the "My Properties" tab.
Registered users will also be able to edit, delete, or share saved reports.
An unregistered user will only be able to create and view reports. 

![Imgur Image](https://i.imgur.com/x9YMgab.png)

## Lessons Learned
This project taught me more than just programming. I developed my skills such as resourcefulness, self sufficiency, and persistence. 

Besides the Bootstrap CSS template, this entire application was built from scratch. 
There was no tutorial to guide me from step A to Z.
Instead, I was forced to break down large problems into smaller chunks, solve the smaller problems, and put it all back together.
I learned how frustrating bugs can be, wanting to quit midway, but pushing through a successful feature implementation.
I learned how to set deadlines so the project would not drag on indefinitely and how to use project management software such as Trello to track all outstanding items.  

The time spent on this project was ~2.5 months, which included a few hours everyday after work (Monday - Friday) and 4-8 hours on (Saturday/Sunday). 
The estimated total time to completion was 180 hours. 

With this experience, I am confident that I can learn new technologies for any project.

Technical skills utilized during this project:
- Python
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

