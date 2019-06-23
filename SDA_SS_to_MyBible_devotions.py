#! /usr/bin/env python3
# encoding: utf-8
""" SDA Sabbath school MyBible module generator

This program creates MyBible devotions modules from data from adventech.io
"""

import os
import argparse
import datetime
import regex
import sqlite3
import requests

from bs4 import BeautifulSoup

import bible_codes
from code import interact
from sqlalchemy.sql.expression import false

DEBUG_LEVEL = 0

class internat:
    lang_code = 'en'
    db_info_description = {\
        "en":"Seventh-day Adventist Church`s Sabbath School lessons",\
        "ru":"Пособие по изучению Библии в Субботней школе церкви Христиан адвентистов седьмого дня",\
        "uk":"Посібник з вивчення Біблії в Суботній школі церкви адвентистів сьомого дня",\
        }
    db_info_description_version_adult = {\
        "en":"for adults",\
        "ru":"для взрослых",\
        "uk":"для дорослих",\
        }
    db_info_description_version_youth = {\
        "en":"for youth",\
        "ru":"для молодёжи",\
        "uk":"для молоді",\
        }
    list_of_quarterly_themes = {\
        "en":"List of quarterly themes:",\
        "ru":"Список тем кварталов:",\
        "uk":"Список тем кварталів:",\
        }
    from_author = {\
        "en":"""To send bugs and wishes on the module, use the service at <a href="https://github.com/Juzujka/SDA_SS_to_MyBible/issues"> https://github.com/Juzujka/SDA_SS_to_MyBible/issues </a>. Thanks, blessings, suggestions for help and cooperation send to juzujka@gmail.com.""",\
        "ru":"""Для отправки замечаний и пожеланий по модулю воспользуйтесь сервисом по адресу <a href="https://github.com/Juzujka/SDA_SS_to_MyBible/issues">https://github.com/Juzujka/SDA_SS_to_MyBible/issues </a>. Благодарности, благословения, предложения о помощи и сотрудничестве присылайте на juzujka@gmail.com.""",\
        "uk":"""Для відправки зауважень і побажань по модулю скористайтесь сервісом за адресою <a href="https://github.com/Juzujka/SDA_SS_to_MyBible/issues">https://github.com/Juzujka/SDA_SS_to_MyBible/issues </a>. Подяки, благословення, пропозиції про допомогу і співробітництво надсилайте на juzujka@gmail.com. По можливості, пишіть російською або англійською мовами.""",\
        }
    origin_text = {\
        "en":"""created by Egor Ibragimov, juzujka@gmail.com\nthe text is taken from sabbath-school.adventech.io""",\
        "ru":"""created by Egor Ibragimov, juzujka@gmail.com\nthe text is taken from sabbath-school.adventech.io""",\
        "uk":"""created by Egor Ibragimov, juzujka@gmail.com\nthe text is taken from sabbath-school.adventech.io""",\
        }
    lesson = {\
        "en":"lesson",\
        "ru":"урок",\
        "uk":"урок",\
        }
    day = {\
        "en":"day",\
        "ru":"день",\
        "uk":"день",\
        }
     

class text_material:
    """some text material: text for the day, intro, comments
    
    not realized"""
    content = ""
    title = ""

    def get_content(self, block):
        pass

    def get_title(self, block):
        pass


class intro(text_material):
    """intro for quarter"""

    def get_content(self, quarter):
        pass
    def __init__(self):
        text = ""


class day:
    """material for the day of the lesson (includes text material)
    
    Class gathers and stores content of a lesson for a particular day.

    Attributes
    ----------
    day_N: int
        day number of the lesson to handle, should be from 1 to 7
    day_date: datetime
        date of the lesson to handle
    full_path: str
        path to lesson, it is a link https:// ...
    content: str
        content of reading for a day
    title: str
        title of reading for a day
    lang_code: str
        two-letters code of language of a day, for example 'en', 'ru', 'uk' etc.
    """
    
    # number of a day in a lesson
    day_N = 0
    # date of a day
    day_date = 0
    # web link of a day
    full_path = ""
    # xml content of a day, text with attached information
    content = ""
    # title of material for a day
    title = ""
    # language code of a day
    lang_code = "ru"

    def set_lang_code(self, lang):
        """
        sets language for the day.

        Parameters
        ----------
        lang: str
            two-letter code of language of a day, for example 'en', 'ru', etc.
        """
        self.lang_code = lang

    def get_content(self, full_path: str, day_N: int):
        """get reading for day

        method calls http request,
        parses and extracts content and title of reading for day.

        Parameters
        ----------
        full_path: str
            path to lesson, it is a link https:// ...
        day_N: int
            number of day of the lesson to handle, should be from 1 to 7"""
        
        # set values of attributes to values of parameters passed to function
        self.full_path = full_path
        self.day_N = day_N
        # create a link for request by adding tail with link to day to the lesson
        request_str = ("{0}/days/{1:02}/read/index.json")\
            .format(self.full_path, self.day_N)
        # send request and get xml  with day of lesson with its attributes
        r = requests.get(request_str)
        # extract content, date and title
        self.content = r.json().get('content')
        # convert content of the day into format of MyBible
        self.content = adventech_lesson_to_MyBibe_lesson( self.content,
                                                          self.lang_code)
        # extract date from xml and save to attribute
        self.day_date = datetime.datetime.strptime(r.json().get('date'),
                                                    "%d/%m/%Y")
        # extract title from xml and save to attribute
        self.title = r.json().get('title')
class comment(text_material):
    """commentaries for lesson, for sabbath schoo leaders
    
    not realized yet, sources of commentaries needed"""

    def get_content(self, lesson):
        pass


class lesson:
    """lesson (includes days)
    
    class gathers a links for the lessons of the quarter, title of lesson, dates of beginning and end
    
    Attributes
    ----------
    lesson_N: int
        number of lesson in quarter
    lesson_title: str
        title of lesson
    lesson_start, lesson_end: datetime
        date of the beginning and the end of the lesson
    lesson_full_path: str
        link to lesson, https:// ...
    lesson_index: str
        index to lesson in form of adventech.io index
    lesson_block: str
        response of http request with lesson
    days[]: day
        array of days
    lang_code: str
        two-letters code of language of a day, for example 'en', 'ru', 'uk' etc.
    """
    lesson_N = 0
    lesson_title = ""
    lesson_start = datetime.date(2000, 1, 1)
    lesson_end = datetime.date(2000, 1, 1)
    # web address of a lesson
    lesson_full_path = ""
    # index of a lesson in web-address 
    lesson_index = ""
    # xml with lessons parameters
    lesson_block = ""
    # array of day-object of this lesson
    days = []
    # language of lesson
    lang_code = "ru"

    def set_lang_code(self, lang):
        """
        set language for the day.

        Parameters
        ----------
        lang: str
            two-letter code of language of a day, for example 'en', 'ru', etc.
        """

        self.lang_code = lang

    def get_lesson_N(self):
        """ returns number of the lesson in the quarter """
        # print("lesson id {0}".format(lesson_block.get("id")))
        return self.lesson_block.get("id")

    def get_lesson_start(self):
        """ returns date of beginning of the lesson """
        start_string = self.lesson_block.get("start_date")
        # print("start_string {0}".format(start_string))
        return datetime.date(int(start_string.split('/')[2]), \
                             int(start_string.split('/')[1]), \
                             int(start_string.split('/')[0]))

    def get_lesson_end(self):
        """ returns date of end of the lesson """
        end_string = self.lesson_block.get("end_date")
        # print("end_string {0}".format(start_string))
        return datetime.date(int(end_string.split('/')[2]), \
                                 int(end_string.split('/')[1]), \
                                 int(end_string.split('/')[0]))

    def get_lesson_full_path(self):
        """ returns web-address of the lesson"""
        return self.lesson_block.get("full_path")

    def get_lesson_index(self):
        """ returns index of web-address of the lesson """
        return self.lesson_block.get("index")

    def get_lesson_title(self):
        return self.lesson_block.get("title")

    def get_content(self):
        """ extracts data for the lesson
        
        fills attributes of the lesson
        gathers data of each day in the lesson"""
        
        self.lesson_N = int(self.get_lesson_N())
        self.lesson_title = self.get_lesson_title()
        self.lesson_start = self.get_lesson_start()
        self.lesson_end = self.get_lesson_end    ()
        self.lesson_full_path = self.get_lesson_full_path ()
        self.lesson_index = self.get_lesson_index()
        for day_N in range(1, 8):
            # prints number of current lesson and number of current day,
            # it is useful for progress indication 
            print("lesson {0} day {1}".format(self.lesson_N, day_N))
            # creates a new object for the day
            curr_day = day()
            # sets language of the day same as language of the lesson
            curr_day.set_lang_code(self.lang_code)
            # adds current day to the array of days for the lesson
            self.days.append(curr_day)
            # gathers day content for current day,
            # method is called from the object placed in array of days
            # current day now is the last day in array
            self.days[-1].get_content(self.lesson_full_path, day_N)
        pass

    def __init__(self, lesson_block, lesson_N):
        """ create object of lesson
        
        Parameters
        ----------
        lesson_block: text with xml
            response of adventech.io API for lesson request
        lesson_N: int
            number of lesson in quarter
        """
        self.lesson_block = lesson_block
        self.lesson_N = lesson_N
        self.lesson_title = ""
        self.days = []
        

class quarter:
    """quarter (includes lessons)"""

    def set_quarter(self, year, quarter):
        """ sets year of the lesson and the quarter number in the year"""
        self.year = year
        self.quart_N = quarter
        
    def set_lang_code(self, lang):
        self.lang_code = lang

    def set_lesson_type(self, lesson_type):
        """ sets lesson type
        
        Parameters
        ----------
        lesson_type: string
            - ad - adults
            - ay - youth
            - ... as in adventech.io
        """
        self.lesson_type = lesson_type

    def set_db_cursor(self, db_cursor):
        """ set database cursor
        
        sets database cursor to access database
         to read existing information to add new quarter
         to write new data """
        self.db_cursor = db_cursor

    def get_content(self):
        """ gets content of the quarter
        
        prepares gathering data for a lesson and calls gathering methods 
        """
        
        # sets lesson type code for adventech.io request
        lesson_type_string = ""
        if self.lesson_type == "ad":
            lesson_type_string = ""
        else:
            if self.lesson_type == "ay":
                lesson_type_string = "-ay"
        # combines request of quarter from parameters
        request_str = ("{0}/api/v1/{1}/quarterlies/{2}-{3:02}{4}/index.json")\
            .format(self.site, self.lang_code, self.year,
                     self.quart_N, lesson_type_string)
        print("get_content by {0}".format(request_str))
        # sends request to adventech.io
        r = requests.get(request_str)
        # extracts from xml received in response title of lesson, description
        self.quarter_title = r.json().get('quarterly').get('title')
        self.quarter_description = r.json().get('quarterly').get('description')
        print("quarter {0}-{1:02}{2}"\
              .format(self.year, self.quart_N, lesson_type_string))
        print("*** title: {0}".format(self.quarter_title))
        # extracts lessons from xml received in response 
        self.lessons_block = r.json().get('lessons')
        # enumerates lessons in lessons_block to get content from each lesson 
        for index, lesson_block in enumerate(self.lessons_block):
            lesson_block = self.lessons_block[index]
            # creates new lesson and append to array of lessons
            self.lessons_set.append(lesson(lesson_block, index + 1))
            # sets language of a new lesson
            self.lessons_set[-1].set_lang_code(self.lang_code)
            # receives content for the new lesson
            self.lessons_set[-1].get_content()
        pass

    def print_quarter(self):
        """ prints information about quarter, for debugging """
        for index, lesson_item in enumerate(self.lessons_set):
            print("lesson_set[{0}] {1}"\
                  .format(index, self.lessons_set[index].lesson_N))
            print("lesson_set[{0}] {1}"\
                  .format(index, self.lessons_set[index].lesson_title))
            print("lesson_set[{0}] {1}"\
                  .format(index, self.lessons_set[index].lesson_start))
            print("lesson_set[{0}] {1}"\
                  .format(index, self.lessons_set[index].lesson_end))
            print("lesson_set[{0}] {1}"\
                  .format(index, self.lessons_set[index].lesson_full_path))
            print("lesson_set[{0}] {1}"\
                  .format(index, self.lessons_set[index].lesson_index))
            for day in self.lessons_set[index].days:
                print("day {0} is {1}".format(day.day_N, day.content))
        
    # TODO: remove this method
    def create_table_info_x(self, cursor, year, quart, name, lang):
        """ creates table info in database, deprecated """
        ret_val = 0
        origin_text = "'created by Egor Ibragimov, juzujka@gmail.com\n" + \
            " the text is taken from sabbath-school.adventech.io'"
        history_of_changes_text = ""
        language_text = "'{0}'".format(lang)
        description_text = \
        "'Seventh Day Adventist Church`s Sabbath School lesson {0}-{1}'"\
        .format(year, quart)
        detailed_info_text = ""
        exec_string = '''CREATE TABLE IF NOT EXISTS info ( name text, value text)'''
        if DEBUG_LEVEL > 0:
            print ("execute db : {0}".format(exec_string))
        cursor.execute(exec_string)
        exec_string = "INSERT INTO info VALUES ( 'origin', {0} )".format(origin_text)
        if DEBUG_LEVEL > 0:
            print ("execute db : {0}".format(exec_string))
        cursor.execute(exec_string)
        exec_string = """INSERT INTO info VALUES ( 'description', {0} )""".format(description_text)
        if DEBUG_LEVEL > 0:
            print ("execute db : {0}".format(exec_string))
        cursor.execute(exec_string)
        exec_string = "INSERT INTO info VALUES ( 'language', {0} )".format(language_text)
        if DEBUG_LEVEL > 0:
            print ("execute db : {0}".format(exec_string))
        cursor.execute(exec_string)
        return(ret_val)

    def __init__(self):
        """the constructor"""
        print("create : quarter :")
        self.site = "https://sabbath-school.adventech.io"
        self.year = 0
        self.quart_N = 0
        self.lang_code = "ru"
        self.lesson_type = "ad"
        #intro = intro()
        self.lessons_block = None
        self.lessons_set = []
        self.quarter_title = ""
        self.quarter_description = ""
        self.db_cursor = None
        pass

class SS_year:
    """ year class (includes quarters)
    
    """
    # array of records of the quarter in xml response from adventech.io
    quarters_list_year = []
    # array of the quarter objects
    quarters = []
    site = "https://sabbath-school.adventech.io"
    lang_code = "ru"
    lesson_type = 'ad'
    quarters_list_year = []
    def set_lang_code(self, lang):
        self.lang_code = lang
    def set_lesson_type(self, lesson_type):
        """ set lesson type
        
        Parameters
        ----------
        lesson_type: string
            - ad - adults
            - ay - youth
            - ... as in adventech.io
        """
        self.lesson_type = lesson_type
    def set_year(self, year):
        self.year = year
    def get_quarters_list(self):
        """ gets a list of quarters from the server """
        self.quarters_list_year = []
        # creates request to adventech.io from attributes
        request_str = ("{0}/api/v1/{1}/quarterlies/index.json")\
            .format(self.site, self.lang_code, self.year)
        print("get_quarters_list with {0}".format(request_str))
        # sends request to the server
        r = requests.get(request_str)
        # selects quarters for the year and appends it to the quarters array
        for index, quart in enumerate(r.json()):
            quart = r.json()[index]
            # select quarters for this year, exclude youth sabbath school to avoid repeating of quarters
            if (int(quart.get("id").split("-")[0])
                == self.year and len(quart.get("id").split("-")) == 2):
                self.quarters_list_year.append(quart)
        print(" quarters for selected year: ")
        # sorts quarters in array by quarter number
        self.quarters_list_year.sort(key = lambda quart_rec:
                                      quart_rec.get("id").split("-")[1])
        for quart in self.quarters_list_year:
            print("quarter {0}".format(quart.get("id")))
        print()
    def get_content(self):
        """ gets content of the year
        
        creates quarter objects with appropriate parameters
        for every quarter in quarters_list_year
        and gets content of every quarter """
        print("SS_year: get content")
        print("self.quarters {0}".format(self.quarters))
        # enumerates quarters elements in quarters_list_year
        for quart in self.quarters_list_year:
            print("process quarter {0}".format(quart.get("id")))
            # creates a new quarter object
            self.quarters.append(quarter())
            # sets parameters of the quarter: year and the quarter number, 
            self.quarters[-1].set_quarter(self.year,
                                           int(quart.get("id").split("-")[1]))
            # sets language
            self.quarters[-1].set_lang_code(self.lang_code)
            # sets lesson type
            self.quarters[-1].set_lesson_type(self.lesson_type)
            # sends requests chain to get content of each day
            self.quarters[-1].get_content()

        
    def __init__(self):
        self.year = 0
        self.site = "https://sabbath-school.adventech.io"
        self.lang_code = "ru"
        self.quarters_list_year = []
        self.quarters = []

class db_MyBible_devotions_SS:
    """ database with devotions (one devotion - one year) """
    # default parameters
    lang_code = 'ru'    # language code for sabbath school text
    lesson_type = 'ad'  # type of lesson: adult, youth etc.
    SS_year_inst = SS_year()    # year class object
    year = 0
    # name of the database file
    file_name = ""
    # year in the database
    db_end_year = -1
    # the last quarter in the database
    db_end_quart = -1
    # the variable stores the result of the check if the file
    # with the name file_name is the file with devotions
    db_inp_file_is_SDA_SS_devotions = False
    # the last day in the database
    db_last_day = 0
    #TODO: remove this method
    def lesson_type_to_text_x(self):
        """ returns text description of type of the lesson """
        lesson_type_descr = "unknown"
        if self.lesson_type == 'ad':
            lesson_type_descr = 'adult'
        if self.lesson_type == 'ay':
            lesson_type_descr = 'youth'
        return lesson_type_descr
    def set_lang_code(self, lang):
        self.lang_code = lang
        self.SS_year_inst.set_lang_code(lang)
    def set_lesson_type(self, lesson_type):
        self.lesson_type = lesson_type
        self.SS_year_inst.set_lesson_type(self.lesson_type)
    def set_year(self, year):
        self.year = year
        self.SS_year_inst.set_year(self.year)
    def get_def_file_name(self):
        """ returns default file name of the database """
        file_name = "SS-{0}-{1}'{2}.devotions.SQLite3"\
            .format(self.lang_code, self.lesson_type, str(self.year)[2:4])
        return file_name
    def connect_to_db(self, file_name):
        """ opens the database in file_name and checks if it is an appropriate devotions"""
        
        # checks year passed in parameters
        if (self.year >= 1852 and self.year <= 2099):
            # if file name is empty it uses default file name
            if (file_name == ""):
                self.file_name = self.get_def_file_name()
            else:
                self.file_name = file_name
            # checks if the file with file_name exists
            if (os.path.isfile(self.file_name)):
                try:
                    # tries to open file_name as database
                    self.db_conn = sqlite3.connect(self.file_name)
                    self.db_cursor = self.db_conn.cursor()
                    print("connection : {0} ; cursor : {1}"\
                          .format(self.db_conn, self.db_cursor))
                    print("sqlite3 version {0}".format(sqlite3.version))
                    ret_val = 1
                except sqlite3.Error as e:
                    print(e)
                    err_name = "creating the database ends with error {0}".format(e)
                    ret_val = -1
                if (ret_val == 1):
                    #processes input file
                    try:
                        # checks is it SDA Sabbath School devotions
                        self.db_cursor.execute("SELECT * FROM info WHERE name = 'description'")
                        info_description = self.db_cursor.fetchall()
                        # checks description
                        if (info_description[0][1].startswith(internat.db_info_description[self.lang_code])):
                            self.db_inp_file_is_SDA_SS_devotions = True
                            print("it is the SDA Sabbath School devotion database")
                            # finds the last quarter in the database
                            self.db_cursor.execute("SELECT * FROM devotions WHERE devotion LIKE '<h3>%'")
                            devotion_quart_heads = self.db_cursor.fetchall()
                            for index, value in enumerate(devotion_quart_heads):
                                (self.db_end_year, self.db_end_quart) = value[1][4:10].split('-')
                                self.db_end_year = int(self.db_end_year)
                                self.db_end_quart = int(self.db_end_quart)
                            print("db_end is {0} - {1}".format(self.db_end_year, self.db_end_quart))
                            # finds the last day in the database
                            self.db_cursor.execute("SELECT MAX(day) FROM devotions")
                            self.db_last_day = self.db_cursor.fetchall()[0][0]
                            print("the last day in the database is {0}".format(self.db_last_day))
                            if (not(self.db_end_year == self.year)):
                                ret_val = -3
                                print("year inconsistent, passed through arguments: {0}, in database of input file {1}"\
                                      .format(self.year, self.db_end_year))
                    except sqlite3.Error as e:
                        ret_val = -2
                        print("error in processing SELECT  info from database : {0}", e)
                        print("file will be cleared and created from the beginning")
                        self.db_end_year = -1
                        self.db_end_quart = -1
            else:
                print("Error: unable to connect to {0}, file not exist".format(self.file_name))
                ret_val = -4
                self.err_name = "file not exist"
        else:
            print("set correct year 1852...2099, {0} is outside".format(self.year))
            ret_val = -5
            self.err_name = "incorrect year"
        return(ret_val)
    def create_db(self, file_name):
        """ creates a new database with devotions 
        in file with name file_name if field file_name not empty
        or use default file name """
        # checks year
        if (self.year >= 1852 and self.year <= 2099):
            # if file_name is empty then default file name will be used
            if (file_name == ""):
                self.file_name = self.get_def_file_name()
            else:
                self.file_name = file_name
            print("creating the database with the file name {0}".format(self.file_name))
            # checks if file with file_name is exists
            if (not(os.path.isfile(self.file_name))):
                # creates file with name file_name with database
                try:
                    self.db_conn = sqlite3.connect(self.file_name)
                    self.db_cursor = self.db_conn.cursor()
                    print("connection : {0} ; cursor : {1}"\
                          .format(self.db_conn, self.db_cursor))
                    print("sqlite3 version {0}".format(sqlite3.version))
                    ret_val = 1
                except sqlite3.Error as e:
                    print(e)
                    self.err_name = "error while creating database : {0}".format(e)
                    ret_val = -1
            else:
                # if file file_name exists, then returns with error
                print("Error: file already exists")
                self.err_name = "file already exists"
                ret_val = -4
        else:
            print("set correct year 1852...2099, please, {0} is outside".format(self.year))
            ret_val = -5
            self.err_name = "incorrect year"
        return(ret_val)

    def get_year(self):
        """ returns list of quarters in the year """
        self.SS_year_inst.set_year(self.year)
        self.SS_year_inst.set_lang_code(self.lang_code)
        self.SS_year_inst.set_lesson_type(self.lesson_type)
        self.SS_year_inst.get_quarters_list()
    def get_content(self):
        """ sends chain of requests to get content of days """
        self.SS_year_inst.get_content()
    def get_db_description_text(self):
        """
        returns description text
        
        function returns description text for the database file of the lesson in selected language
        it substitutes
         - the name of material - Seventh-day Adventist Church`s Sabbath School lessons
         - the year and the quarter
         - the version: for adults or for youth
        """
        
        # sets description text in different languages
        # default value is English
        # sets header of devotion
        # sets description of type of lesson
        name_text = internat.db_info_description[self.lang_code]
        if (self.lesson_type == 'ad'):
            version_text = internat.db_info_description_version_adult[self.lang_code]
        else:
            if (self.lesson_type == 'ay'):
                version_text = version_text = internat.db_info_description_version_youth[self.lang_code]
            else:
                version_text = ""
        description_text = "{0} {1} {2}".format(name_text, version_text, self.SS_year_inst.quarters_list_year[-1].get('id'))
        return  description_text
    def get_db_detailed_info_text(self):
        """ returns detailed info in selected languages """
        #TODO: add list of quarters from the beginning of the year to the current quarter
        themes_list = "<p> {0} </p>".format(internat.list_of_quarterly_themes[self.lang_code])
        for quarter in self.SS_year_inst.quarters:
            themes_list = themes_list + "<h4>" + "{0}.".format(quarter.quart_N) + " " + quarter.quarter_title + "</h4>"# + "<p>" + quarter.quarter_description + "</p>"
        from_author_of_module_text = internat.from_author[self.lang_code]
        detailed_info_text = "{0}<br><p>{1}</p>".format(themes_list, from_author_of_module_text)
        return detailed_info_text
    def create_table_info(self):
        """ creates table 'info' for the MyBible devotion database"""
        ret_val = 0
        origin_text = internat.origin_text[self.lang_code]
        history_of_changes_text = "2018-06-30 - created"
        language_text = "{0}".format(self.lang_code)
        detailed_info_text = ""
        if self.lang_code == "ru" or self.lang_code == "uk":
            russian_numbering_text = "{0}".format('true')
        else:
            russian_numbering_text = "{0}".format('false')
        exec_string = '''CREATE TABLE IF NOT EXISTS info ( name text, value text)'''
        if DEBUG_LEVEL > 0:
            print ("execute db : {0}".format(exec_string))
        self.db_cursor.execute(exec_string)
        exec_string = '''DELETE from info'''
        if DEBUG_LEVEL > 0:
            print ("execute db : {0}".format(exec_string))
        self.db_cursor.execute(exec_string)
        exec_string = "INSERT INTO info VALUES ( 'origin', '{0}' )".format(origin_text)
        if DEBUG_LEVEL > 0:
            print ("execute db : {0}".format(exec_string))
        self.db_cursor.execute(exec_string)
        exec_string = """INSERT INTO info VALUES ( 'description', '{0}' )""".format(self.get_db_description_text())
        #exec_string = """INSERT INTO info VALUES ( 'description', '{0}' )""".format(internat.db_info_description[self.lang_code])
        if DEBUG_LEVEL > 0:
            print ("execute db : {0}".format(exec_string))
        self.db_cursor.execute(exec_string)
        exec_string = """INSERT INTO info VALUES ( 'detailed_info', '{0}' )""".format(self.get_db_detailed_info_text())
        if DEBUG_LEVEL > 0:
            print ("execute db : {0}".format(exec_string))
        self.db_cursor.execute(exec_string)
        exec_string = "INSERT INTO info VALUES ( 'language', '{0}' )".format(language_text)
        if DEBUG_LEVEL > 0:
            print ("execute db : {0}".format(exec_string))
        self.db_cursor.execute(exec_string)
        exec_string = "INSERT INTO info VALUES ( 'russian_numbering', '{0}' )".format(russian_numbering_text)
        if DEBUG_LEVEL > 0:
            print ("execute db : {0}".format(exec_string))
        self.db_cursor.execute(exec_string)
        return(ret_val)
    def update_description(self):
        """ updates description of the existing database """
        exec_string = "DELETE FROM info WHERE name='description'" 
        if DEBUG_LEVEL > 0:
            print ("execute db : {0}".format(exec_string))
        self.db_cursor.execute(exec_string)
        exec_string = """INSERT INTO info VALUES ( 'description', '{0}' )""".format(self.get_db_description_text())
        if DEBUG_LEVEL > 0:
            print ("execute db : {0}".format(exec_string))
        self.db_cursor.execute(exec_string)
    def update_detailed_info(self):
        """ update detailed_info of the existing database """
        exec_string = "DELETE FROM info WHERE name='detailed_info'" 
        if DEBUG_LEVEL > 0:
            print ("executing db : {0}".format(exec_string))
        self.db_cursor.execute(exec_string)
        exec_string = """INSERT INTO info VALUES ( 'detailed_info', '{0}' )""".format(self.get_db_detailed_info_text())
        if DEBUG_LEVEL > 0:
            print ("executing db : {0}".format(exec_string))
        self.db_cursor.execute(exec_string)
    def create_table_devotions(self):
        """ writes days from gathered days in lessons in quarters in year into the database"""
        
        exec_string = '''CREATE TABLE IF NOT EXISTS devotions (day NUMERIC, devotion TEXT)'''
        if DEBUG_LEVEL > 0:
            print ("executing db : {0}".format(exec_string))
        self.db_cursor.execute(exec_string)
        exec_string = '''CREATE UNIQUE INDEX IF NOT EXISTS devotions_index ON devotions (day ASC)'''
        if DEBUG_LEVEL > 0:
            print ("executing db : {0}".format(exec_string))
        self.db_cursor.execute(exec_string)
        # the day after the last day in the database is the first day of current quarter
        # set days_counter to number of the last day in the database plus 1
        days_counter = self.db_last_day + 1
        lesson_counter = 1
        print("the number of the quarters is {0}".format(len(self.SS_year_inst.quarters)))
        for quarter in self.SS_year_inst.quarters:
            print("the length of the lesson_set array is {0}".format(len(quarter.lessons_set)))
            for lesson in quarter.lessons_set:
                print("lesson N {0:2} - {1:2}".format(lesson_counter, lesson.lesson_N))
                #print("length of the days array is {0}".format(len(lesson.days)))
                # days_accumulator concatenates html for the current day
                # in the beginning and in the end of the year it is possible that days are considers days of current quarter from the year before and the year after the current year 
                days_accumulator = ""
                for day in lesson.days:
                    # day starts from a lesson number and a header
                    day_content_handled = "<p>  {0} № {1} {2} {3}</p> <h4>{4}</h4> {5}".format(internat.lesson[self.lang_code], str(lesson.lesson_N), internat.day[self.lang_code], str(day.day_N), day.title, day.content)
                    exec_string = '''INSERT INTO devotions VALUES ( ?, ? )'''
                    if DEBUG_LEVEL > 0:
                        print ("executing db : {0}".format(exec_string))
                    # if it is the first day in the quarter then add a quarter title and a quarter description 
                    if (lesson.lesson_N == 1 and day.day_N == 1):
                        days_accumulator = "<h3>" + "{0}-{1}".format(quarter.year, quarter.quart_N) + " " + quarter.quarter_title + "</h3>" + "<p>" + quarter.quarter_description + "</p>" +  days_accumulator
                    days_accumulator = days_accumulator + day_content_handled
                    # if the current day is not in current year then keep current day in the days_accumulator
                    if (day.day_date.year == self.year):
                        # if the current day is in current year then put day into database and clear days_accumulator
                        print( "put day {0}: ".format(days_counter))
                        self.db_cursor.execute(exec_string, (days_counter, days_accumulator))
                        days_accumulator = ""
                        days_counter += 1
                    else:
                        print("move the day {0} to the next day".format(day.day_date))
                lesson_counter += 1
        pass
    def close_db(self):
        if (self.db_conn):
            print("close database")
            self.db_conn.commit()
            self.db_conn.close()

    def __init__(self):
        self.year = 0
        self.err_name = ""
        self.file_name = ""
        self.db_conn = None
        self.db_cursor = None

    def __del__(self):
        self.close_db()

def ref_tag_preprocess_en(inp_tag_text):
    """ function adopts references
    references in lessons in English are specific
    """
    
    # replaces "see also" with spaces
    inp_tag_text = inp_tag_text.replace("see also", " ")
    # replaces "Song of Solomon" with "Song"
    inp_tag_text = inp_tag_text.replace("Song of Solomon", "Song")
    # finds books with names starts with digit, adds separator ';' before book name
    # because of references divided with commas, it is difficult to separate book name from previous reference
    # this part of code searches every name which starts from digit in reference
    # and adds ';' symbol before book names was found

    # enumerate all references from dictionary of book names
    for i1, (key, val) in enumerate(bible_codes.book_index_to_MyBible['en'].items()):
        # if it is a book name starting from digit
        if (key[0].isdigit()):
            # add space before and after the digit
            templ_to_search = " " + key[0] + " " + key[1:]
            # replace space before digit with '&',
            # so others variants of name  of this book which whould be found
            # will not modify this part again
            templ_replacing = "&" + key[0] + " " + key[1:]
            inp_tag_text = inp_tag_text.replace(templ_to_search, templ_replacing)
        # now all digit-starting book names are separated with '&'
        # removes comma between references
        inp_tag_text = inp_tag_text.replace(",&", " &")
        # next is replacing '&' with ';'
        inp_tag_text = inp_tag_text.replace("&", "; ")
    return inp_tag_text

def ref_tag_preprocess_ru(inp_tag_text):
    """adopting references in lessons in Russian"""
    
    # some words in references
    #TODO: fix "see also"
    inp_tag_text = inp_tag_text.replace("see also", " ")
    # long book name for Song of Solomon
    inp_tag_text = inp_tag_text.replace("Песнь Песней", "Песн.")
    inp_tag_text = inp_tag_text.replace("Песни Песней", "Песн.")
    return inp_tag_text

def adventech_ref_to_MyBible_ref(lang_code, doc, inp_tag):
    """ find bible references and convert to MyBible format"""

    # regular expression for selecting reference to book name with verses in particular book
                            #   /  book name                                         \ /    head, verse repeatable after selected book name                                                                                    \ 
    find_refs = regex.compile(r"(?:\d\s*)?(?:[\p{Lu}]\.\s)?[\p{Lu}]?[\p{Ll}\’\']+\.?\s*(?:\d+(?:[\:\-\,]\d+)?(?:\s*[\-\,]\s*\d+)?(?::\d+|(?:\s*[\p{Lu}]?[\p{Ll}\’\']+\s*\d+:\d+))?(?:\,\s*)?)*")

    # regular expression for selecting book name from reference with book name, head and verse
    parse_ref = regex.compile(r"(?:\d\s*)?(?:[\p{Lu}]\.\s)?[\p{Lu}]?[\p{Ll}\’\']+")

    #in texts on English references divided by commas. book 1:2 , 1 Cor sees as book1:2,1   Cor.  
    #adding separators before names of numerated books
    
    # replacing "and" in Russian, Ukrainian, English languages to ";"
    # for simplifying handling 
    inp_tag_text = inp_tag.get_text()
    if (lang_code == 'en'):
        inp_tag_text = ref_tag_preprocess_en(inp_tag_text)
    if (lang_code == 'ru'):
        inp_tag_text = ref_tag_preprocess_ru(inp_tag_text)
    ref_tag_preprocess_ru
    inp_tag_text = inp_tag_text.replace(" и ", "; ")
    inp_tag_text = inp_tag_text.replace(" і ", "; ")
    inp_tag_text = inp_tag_text.replace(" and ", "; ")
    inp_tag_text = inp_tag_text.replace(" und ", "; ")
    inp_tag_text = inp_tag_text.replace("–", "-")
    # replacing "'" to "’", it is similar in Ukrainian
    inp_tag_text = inp_tag_text.replace("'", "’")
    inp_tag_text = inp_tag_text + ";"
    #split references into list of references to add book names to references without book name
    inp_tag_list = inp_tag_text.split(";")
    # initializes variables
    inp_tag_text = ""   # text will be rewrote
    book_name = "-"
    for i_elem in range (0, len(inp_tag_list)):     # enumerates elements in list of references
        end_alpha_n = -1            # here will be stored end of part with letters is the end of book name
        elem_not_empty = False      # here will be stored mark of emptiness of element for skipping empty elements
        for (i_lett) in range(0, len(inp_tag_list[i_elem])):            # enumerates letters in reference
            if (inp_tag_list[i_elem][i_lett].isalpha() or inp_tag_list[i_elem][i_lett] == "."): # is it part of book name?
                end_alpha_n = i_lett                                                            # moves position of the end of book name
            if (not(elem_not_empty) and (inp_tag_list[i_elem][i_lett].isalpha() or inp_tag_list[i_elem][i_lett].isdigit())):
                elem_not_empty = True                                                           # marks element as not empty
        if (elem_not_empty):                                            # handles not empty element
            if end_alpha_n > 0 :                                        # here is book name
                book_name = inp_tag_list[i_elem][0:end_alpha_n + 1]     # remembers it for possible using for next reference
            else:                                                       # here is no book name
                inp_tag_list[i_elem] = book_name + inp_tag_list[i_elem] # add book name from previous reference with book name
            inp_tag_text = inp_tag_text + ";" + inp_tag_list[i_elem]    # add not empty element to the end of the string with references
    # collect to refs all references to Bible texts
    refs = find_refs.findall(inp_tag_text)
    if (DEBUG_LEVEL > 0):
        print("process doc {0},\n tag {1}, \n inp_tag_text {2}".format(doc, inp_tag, inp_tag_text))
        print("find_refs {0}".format(refs))
        print(" * references: *")

    # insert ";" between references, do not insert in the end
    is_last_ref = True          #mark: it is the end reference, beginning from the end 

    book_name = "" 
    # process references from end to beginning
    # to not to process result of processing
    for ref in reversed(refs):
        book_name_parse_ref = parse_ref.match(ref)
        if (book_name_parse_ref == None):
            #there is reference without book name, take the last found book name
            ref = book_name + ref
        book_name_parse_ref = parse_ref.match(ref)
        book_name_parse_ref_group = book_name_parse_ref.group()
        book_name = book_name_parse_ref_group.replace(" ", "")
        book_name_as_list = list(book_name)
        book_name_as_list[0] = book_name_as_list[0].upper()
        book_name_to_find = "".join(book_name_as_list)
        book_N = bible_codes.book_index_to_MyBible[lang_code].get(book_name_to_find)
        if (book_N == None):
            print("! referense not recognised, refs : {0} ; ref {1}; book name {2}".format(refs, ref, book_name))
            #print("doc: {0}".format(doc))
        if (DEBUG_LEVEL > 0):
            print("ref: {0} parsed is {1} name is {2}, N is {3}".format(ref, parse_ref.match(ref), book_name, book_N))
        numeric_part = (ref[parse_ref.match(ref).span()[1] + 1:]).replace(" ", "")
        # if numeric part includes list of verses separated by commas like "Mt. 1:2-4, 5, 7, 9" then divide into list of references
        numeric_part_list = numeric_part.split(",")                 # divides reference into parts
        numeric_part_list = list(filter(None, numeric_part_list))   # removes empty strings from list
        # convert consecutive number into range
        to_continue = len(numeric_part_list) > 1    # initializes mark to continue by checking after current element there is one or more elements
        ind = 0                                     # index of the current element
        while(to_continue):
            repeat_index = False                    # if found incorrect part then deletes it and repeat without it
            if (numeric_part_list[ind]) == "":      # checks if it is empty element
                del numeric_part_list[ind]          # deletes empty element
            else:
                if (numeric_part_list[ind].find(":") >= 0):             # checks is it element with head number
                    verse_part = numeric_part_list[ind].split(":")[1]   # if it is then remembers part with verses, it is after ":"
                else:
                    verse_part = numeric_part_list[ind]                 # else all element is verses
                try:
                    if (verse_part.find("-") >= 0):                         # checks element is range
                        range_end_number = int(verse_part.split("-")[1])    # if it is then remembers end of range, it will be used to concatenating with next verses
                    else:
                        range_end_number = int(verse_part)                  # if it is not range, then it is a single verse and it is the end of range itself
                except ValueError:
                    print("incorrect verse found while handling {0}".format(inp_tag))   # print error message and diagnostic information
                    print("reference is {0}".format(ref))
                    print("numeric part is {0}; verse part is not integer: {1}".format(numeric_part_list[ind], verse_part))
                    del numeric_part_list[ind]                              # deletes incorrect element
                    repeat_index = True
                if not(repeat_index):
                    if (ind < len(numeric_part_list) - 1):  # current element is not the last element
                        if (numeric_part_list[ind + 1].find("-") >= 0 or numeric_part_list[ind + 1].find(":") >= 0): # next element is range or in new head, skip
                            pass
                        else:
                            try:
                                numeric_part_next_value = int(numeric_part_list[ind + 1])
                            except ValueError:
                                print("incorrect verse found while handling {0}".format(inp_tag))   # print error message and diagnostic information
                                print("reference is {0}".format(ref))
                                print("numeric part in next element branch is {0}".format(numeric_part_list[ind + 1]))
                                del numeric_part_list[ind + 1]                              # deletes incorrect element
                                repeat_index = True
                            if not(repeat_index):
                                if (numeric_part_next_value == (range_end_number + 1)):
                                    if (numeric_part_list[ind].find("-") >= 0): # element is range
                                        numeric_part_list[ind] = numeric_part_list[ind].split("-") + "-" + numeric_part_list[ind + 1]
                                    else:
                                        numeric_part_list[ind] = numeric_part_list[ind] + "-" + numeric_part_list[ind + 1]
                                    del numeric_part_list[ind + 1]
            if (ind < len(numeric_part_list) - 1):  # checks if it is element after current element
                if not(repeat_index):               # if element deleted then keep current value of index, it points to the next element
                    ind = ind + 1                   # increment index for handling the next element 
            else:
                to_continue = False                 # if it is the last element then finishes
    
                        
        # and add head numbers to verses
        if len(numeric_part_list) > 1: # if it is a reference with heads only then skip
            head_number = ""
            for i1, numeric_part_elem in enumerate(numeric_part_list) :
                if (numeric_part_elem.find(":") >= 0):                      # element considers head number
                    head_number = numeric_part_elem.split(":")[0]           # remembers head number
                else :
                    numeric_part_list[i1] = head_number + ":" + numeric_part_elem   # add head number if there is no head number
            
        # concatenate reference from reference header "B:",
        # book number and head number with verse number
        for numeric_part_elem in reversed(numeric_part_list) :
            if (book_N == 380 or book_N == 700 or book_N == 710 or book_N == 720 or book_N == 640):
                # if book Obadiah or 2 John or 3 John or Jude or Philemon,
                # which has one head then add to the reference head one "1:"
                MyBible_ref = "B:{0} 1:{1}".format(book_N, numeric_part_elem)
            else:
                MyBible_ref = "B:{0} {1}".format(book_N, numeric_part_elem)
            # if reference considers comma separated list then divide list into list of references
            
            if (DEBUG_LEVEL > 0):
                print("MyBible ref: {0}".format(MyBible_ref))
            MyBible_a_tag = doc.new_tag("a", href=MyBible_ref)
            MyBible_a_tag.insert(0, "{0}.{1}".format(book_name, numeric_part_elem))
            # add ; between references
            if not(is_last_ref):
                inp_tag.insert_after("; ")
            inp_tag.insert_after(MyBible_a_tag)
            is_last_ref = False
    inp_tag.decompose()

        
def adventech_lesson_to_MyBibe_lesson(doc, lang_code):
    """ convert lesson to MyBible format

     parses lesson material,
     finds Bible references
     and replaces with Bible references in MyBible format"""

    doc_soup = BeautifulSoup(doc, 'html.parser')
    if (DEBUG_LEVEL > 0):
        print ('anchors')
    # find all elements with tag <a> and class "verse"
    anchors = doc_soup.find_all('a', class_='verse')

    # process all verses with adventech_ref_to_MyBible_ref function
    for item in list(anchors):
        if (DEBUG_LEVEL > 0):
            print("item")
            print(item)
        bible_verses = item.get_text()
        if (DEBUG_LEVEL > 0):
            print("bible verses: {0}".format(bible_verses))
        adventech_ref_to_MyBible_ref(lang_code, doc_soup, item)
    doc = str(doc_soup)
    return(doc)
    
if __name__ == '__main__':
    # process command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--year"  ,   type = int, help="year for lessons", default = -1)
    parser.add_argument("-a", "--append",   action = "store_true", help = "add new lessons to the end of existing database", default = False)
    parser.add_argument("-o", "--db_file",  help = "name of database output file", default = "")
    parser.add_argument("-l", "--list"  ,   action = "store_true", help = "get list of available quarters", default = False)
    parser.add_argument(      "--lang"  ,   action = "store",      help = "language", default = "ru")
    parser.add_argument(      "--type"  ,   action = "store",      help = "type of lesson: ad - adult, ay - youth", default = "ad")
    parser.add_argument(      "--test"  ,   action = "store_true", default=False)
    parser.add_argument( "--test_print_day"   ,   action = "store_true", help = "print selected day to console", default=False)
    parser.add_argument( "--test_n_quart" ,   type = int, help="quarter for test", default = 1)
    parser.add_argument( "--test_n_less"  ,   type = int, help="lesson for test", default = 1)
    parser.add_argument( "--test_n_day"   ,   type = int, help="day for test", default = 1)
    args = parser.parse_args()

    # check year, first Sabbath school lesson dated by 1852 year
    if (args.year > 1852):
        lesson_year = args.year
    else:
        lesson_year = datetime.datetime.now().year
    print("create MyBible module with SDA Sabbath School lessons on {0} language for year {1}".format(args.lang, args.year))

    # create object of database with Sabbath school devotions 
    devotions = db_MyBible_devotions_SS()
    # set parameters from command line arguments
    devotions.set_year(lesson_year)
    devotions.set_lang_code(args.lang)
    devotions.set_lesson_type(args.type)
    if (args.test):
        print("test")
        #print(get_list_of_1st_digit_book)
        inp_tag = "Ps. 119:105, 2 Tim. 3:16"
        inp_tag = ref_tag_preprocess_en(inp_tag)
        print(inp_tag)
    else:
        if (args.test_print_day) :
            print("test print day")
            # sends requests chain to get content of each day
            #devotions.SS_year_inst.quarters[-1].get_content()
            lesson_type_string = ""
            if args.type == "ad":
                lesson_type_string = ""
            else:
                if args.type == "ay":
                    lesson_type_string = "-ay"
            # combines request of quarter from parameters
            site = "https://sabbath-school.adventech.io"
            request_str = ("{0}/api/v1/{1}/quarterlies/{2}-{3:02}{4}/index.json")\
                .format(site, args.lang, args.year,
                         args.test_n_quart, lesson_type_string)
            print("get_content by {0}".format(request_str))
            # sends request to adventech.io
            r = requests.get(request_str)
            # extracts from xml received in response title of lesson, description
            quarter_title = r.json().get('quarterly').get('title')
            quarter_description = r.json().get('quarterly').get('description')
            print("quarter {0}-{1:02}{2}"\
                  .format(args.year, args.test_n_quart, lesson_type_string))
            print("*** title: {0}".format(quarter_title))
            lessons_block = r.json().get('lessons')
            # enumerates lessons in lessons_block to get content from each lesson 
            lesson_block = lessons_block[args.test_n_less - 1]
            # creates new lesson and append to array of lessons
            lesson = lesson(lesson_block, args.test_n_less)
            # sets language of a new lesson
            lesson.set_lang_code(args.lang)
            # receives content for the new lesson
            #lesson.get_content()
            print("lesson {0} day {1}".format(args.test_n_less, args.test_n_day))
            # creates a new object for the day
            curr_day = day()
            # sets language of the day same as language of the lesson
            curr_day.set_lang_code(args.lang)
            # adds current day to the array of days for the lesson
            # gathers day content for current day,
            # method is called from the object placed in array of days
            # current day now is the last day in array
            curr_day.get_content(lesson_block.get("full_path"), args.test_n_day)
            print("content:")
            print(curr_day.content)

        else:
            if (args.list):
                #get quarters list and print, do not modify or create database file
                devotions.SS_year_inst.get_quarters_list()
            else:
                if(args.append):
                    # selected option of appending new quarters to existing database
                    
                    # try to open file as database
                    if (devotions.connect_to_db(args.db_file) > 0):
                        # get list of available quarters from server
                        devotions.SS_year_inst.get_quarters_list()
                        # check if new quarters are available?
                        if (len(devotions.SS_year_inst.quarters_list_year) <= devotions.db_end_quart):
                            print("nothing to add")
                        else:
                            # remove from list the quarters which are already in database
                            for i in range(0, devotions.db_end_quart):
                                devotions.SS_year_inst.quarters_list_year.pop(0)
                            print ("list of quarters to add")
                            # print quarters which will be added
                            for index, i_quarter in enumerate(devotions.SS_year_inst.quarters_list_year):
                                print(i_quarter.get('id'))
                            #get quarters
                            print ("-- get content --")
                            devotions.SS_year_inst.get_content()
                            #append quarters
                            print ("-- update_description() --")
                            devotions.update_description()
                            print ("-- update_detailed_info() --")
                            devotions.update_detailed_info()
                            print ("-- create_table_devotions --")
                            devotions.create_table_devotions()
                    else:
                        print("unable to open file with database {0}".format(args.db_file))
                else:
                    # create file with database
                    if(devotions.create_db(args.db_file) > 0):
                        # get list of available quarters
                        devotions.SS_year_inst.get_quarters_list()
                        print ("list of quarters to add")
                        # print quarters to add
                        for index, i_quarter in enumerate(devotions.SS_year_inst.quarters_list_year):
                            print(i_quarter.get('id'))
                        # get content of quarters
                        print ("-- get content --")
                        devotions.SS_year_inst.get_content()
                        # create table with info in database file
                        print ("-- create_table_info --")
                        devotions.create_table_info()
                        # create table with devotions in database file
                        print ("-- create_table_devotions --")
                        devotions.create_table_devotions()
                    else:
                        print("Error: unable to create database {0}".format(args.db_file))
            
    # usefull links
    #https://sabbath-school.adventech.io/api/v1/ru/quarterlies/2019-01/lessons/07/days/01/read/index.json
