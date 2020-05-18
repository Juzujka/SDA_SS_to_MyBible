# SDA_SS_to_MyBible

This project produces modules with SDA Church Sabbath School lessons for MyBible application.  
Lessons are devotions for every day.

## Getting started


Download the repository

'''
git clone https://github.com/Juzujka/SDA\_SS\_to\_MyBible.git
'''

or download zip into the local directory.

Run the command like below with desirable arguments


'''
./SDA\_SS\_to\_MyBible\_devotions.py --year 2020 --lang ru --type ad --append
'''

arguments:
 * --year - year of Sabbath School lessons
 * --lang - language code: en, ru, es, uk
 * --type - ad - for adult lessons, ay - for youth lessons
 * --append - if exists, the script will add the new quarter to the existing database

### Prerequisites

Before using this tool must be installed
 * Python3
 * BeautifulSoup python3 package
 * sqlite3 python3 package


### About MyBible_SS

SDA Sabbath school is text materials for study of Bible for every day of a year  
MyBible is Android application for reading Bible with many functions and modules, including devotions for every-day reading.  

SS\_to\_MyBible gathers data from adventech.io service with SDA Sabbath school materials and creates MyBible modules with active links to Bible texts.  

Since MyBible devotions starts with 1st January, the lessons always start from the beginning of the year.
SDA\_SS\_to\_MyBible pulling lessons per quarter from the beginning of the year to the last available quarter.  

The days from previous year of the current lesson added to the first day of current year.  

Introduction added to first day of quarter.  

Data pulled from advantech.io https://github.com/Adventech/adventech.io
