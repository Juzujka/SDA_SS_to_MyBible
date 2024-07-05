# SDA\_SS\_to\_MyBible

This project produces modules with SDA Church Sabbath School lessons for MyBible application. 
Lessons are devotions for every day.

## Getting started


Download the repository

```
git clone https://github.com/Juzujka/SDA\_SS\_to\_MyBible.git
```

or download zip into the local directory.

Install required modules:
```
python3 -m pip install bs4 regex
```
or
```
pip3 install bs4 regex
```

Run the command like below with an appropriate arguments:


```
./SDA\_SS\_to\_MyBible\_devotions.py --year 2020 --lang ru --type ad --append
```

arguments:
 * --year - year of Sabbath School lessons
 * --lang - language code: en, ru, es, uk
 * --type - ad - for adult lessons, ay - for youth lessons
 * --append - if exists, the script will add the new quarter to the existing database

You will get database file of module. If you have recent version of Android then it will be difficult to place this file to the folder of application.
Right way is to publish this file in registry. as descibed in manual (MyBible for Android – extra module registries)[https://mybible.zone/en/android/extra-registries/].
You can use [registry file from this project](https://raw.githubusercontent.com/Juzujka/SDA_SS_to_MyBible/master/SDA-SS-en-ad.devotions.registry.json) and replace links to files in this project to place where your files published.

### Prerequisites

Before using this tool must be installed
 * Python3
 * BeautifulSoup python3 package
 * sqlite3 python3 package


### About SS\_to\_MyBible

SDA Sabbath school is text materials for study of Bible for every day of a year 
MyBible is Android application for reading Bible with many functions and modules, including devotions for every-day reading. 

SS\_to\_MyBible gathers data from adventech.io service with SDA Sabbath school materials and creates MyBible modules with active links to Bible texts. 

Since MyBible devotions starts with 1st January, the lessons always start from the beginning of the year.
SDA\_SS\_to\_MyBible pulling lessons per quarter from the beginning of the year to the last available quarter. 

The days from previous year of the current lesson added to the first day of current year. 

Introduction added to first day of quarter. 

Data pulled from advantech.io https://github.com/Adventech/adventech.io

## How to add modules from this repository to your MyBible application

Open your MyBible application.

Tap three dot in the uper right corner -> tap "Modules" -> tap three dot in the uper right corner -> tap "Extra module registries" -> tap "+" in the upper right corner

Fill URL field with URL of registry file for your language:

Russian - `https://raw.githubusercontent.com/Juzujka/SDA_SS_to_MyBible/master/SDA-SS-ru-ad.devotions.registry.json`
English - `https://raw.githubusercontent.com/Juzujka/SDA_SS_to_MyBible/master/SDA-SS-en-ad.devotions.registry.json`
Spanish - `https://raw.githubusercontent.com/Juzujka/SDA_SS_to_MyBible/master/SDA-SS-es-ad.devotions.registry.json`

If you want Sabbath School module for other language then ask author <juzujka@gmail.com> or make it for yourself as described in section [Getting started](#getting-started).
