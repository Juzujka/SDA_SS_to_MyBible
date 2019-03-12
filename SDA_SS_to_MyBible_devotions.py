#! /usr/bin/env python3
# encoding: utf-8
""" SDA Sabbath school MyBible module generator

This program creates MyBible devotions module from data from adventech.io
"""

import os
import argparse
import datetime
import regex
import sqlite3
import requests

from bs4 import BeautifulSoup

import bible_codes

DEBUG_LEVEL = 0


class text_material:
    """some text material: text for a day, intro, comments
    
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
    """day of lesson (includes text material)
    
    Class gathers and stores content of a lesson for a particular day.

    Attributes
    ----------
    day_N: int
        number of reading for day to handle
    day_date: datetime
        date of reading for day to handle
    full_path: str
        path to lesson, it is address https:// ...
    content: str
        content of reading for day
    title: str
        title of reading for day
    lang_code: str
        two-letters code of language of a day, for example 'en', 'ru', 'uk' etc.
    """
    
    # number of a day in a lesson
    day_N = 0
    # date of a day
    day_date = 0
    # web address of a day
    full_path = ""
    # xml content of a day, text with attached information
    content = ""
    # title of a material for a day
    title = ""
    # language code of a day
    lang_code = "ru"

    def set_lang_code(self, lang):
        """
        set language for a day.

        Parameters
        ----------
        lang: str
            two-letters code of language of a day, for example 'en', 'ru', etc.
        """
        self.lang_code = lang

    def get_content(self, full_path: str, day_N: int):
        """get reading for day

        method calls http request,
        parses and extracts content and title of reading for day.

        Parameters
        ----------
        full_path: str
            path to lesson, it is address https:// ...
        day_N: int
            number of day of week (lesson) to get, 1...7"""
        
        # set values of attributes to values of parameters passed to function
        self.full_path = full_path
        self.day_N = day_N
        # create link for request by adding to lesson tail with address to day
        request_str = ("{0}/days/{1:02}/read/index.json")\
            .format(self.full_path, self.day_N)
        # send request and get xml  with day of lasson with its attributes
        r = requests.get(request_str)
        # extract content, date and title
        self.content = r.json().get('content')
        # convert content of day to format for MyBible
        self.content = adventech_lesson_to_MyBibe_lesson( self.content,
                                                          self.lang_code)
        # extract date from xml and save to attribute
        self.day_date = datetime.datetime.strptime(r.json().get('date'),
                                                    "%d/%m/%Y")
        # extract title from xml and save to attribute
        self.title = r.json().get('title')
class comment(text_material):
    """commentaries for lesson, for class leaders
    
    not realized yet, sources of commentaries needed"""

    def get_content(self, lesson):
        pass


class lesson:
    """lesson (includes days)
    
    class gathers link for lesson, title of lesson, dates of start and end
    
    Attributes
    ----------
    lesson_N: int
        number of lesson in quarter
    lesson_title: str
        title of lesson
    lesson_start, lesson_end: datetime
        date of start end end of lesson
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
        set language for a day.

        Parameters
        ----------
        lang: str
            two-letters code of language of a day, for example 'en', 'ru', etc.
        """

        self.lang_code = lang

    def get_lesson_N(self):
        """ returns number of lesson in quarter """
        # print("lesson id {0}".format(lesson_block.get("id")))
        return self.lesson_block.get("id")

    def get_lesson_start(self):
        """ returns date of beginning of lesson """
        start_string = self.lesson_block.get("start_date")
        # print("start_string {0}".format(start_string))
        return datetime.date(int(start_string.split('/')[2]), \
                             int(start_string.split('/')[1]), \
                             int(start_string.split('/')[0]))

    def get_lesson_end(self):
        """ returns date of end of lesson """
        end_string = self.lesson_block.get("end_date")
        # print("end_string {0}".format(start_string))
        return datetime.date(int(end_string.split('/')[2]), \
                                 int(end_string.split('/')[1]), \
                                 int(end_string.split('/')[0]))

    def get_lesson_full_path(self):
        """ returns web-address of lesson"""
        return self.lesson_block.get("full_path")

    def get_lesson_index(self):
        """ returns index of web-address of lesson """
        return self.lesson_block.get("index")

    def get_lesson_title(self):
        return self.lesson_block.get("title")

    def get_content(self):
        """ extracts data for a lesson
        
        fills attributes of lesson
        gathers data of every day in lesson"""
        
        self.lesson_N = int(self.get_lesson_N())
        self.lesson_title = self.get_lesson_title()
        self.lesson_start = self.get_lesson_start()
        self.lesson_end = self.get_lesson_end    ()
        self.lesson_full_path = self.get_lesson_full_path ()
        self.lesson_index = self.get_lesson_index()
        for day_N in range(1, 8):
            # print number of current lesson and number of current day,
            # it is usefull for progress indication 
            print("lesson {0} day {1}".format(self.lesson_N, day_N))
            # create new object for day
            curr_day = day()
            # set language of day same as language of lesson
            curr_day.set_lang_code(self.lang_code)
            # add current day to array of days for lesson
            self.days.append(curr_day)
            # gather day content for current day,
            # method is called from object placed in array of days
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
        """ set year of lesson and number of quarter in year"""
        self.year = year
        self.quart_N = quarter
        
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

    def set_db_cursor(self, db_cursor):
        """ set database cursor
        
        set database cursor for access to database
         to read existing information for appending new quarter
         to write new data """
        self.db_cursor = db_cursor

    def get_content(self):
        """ get content for quarter
        
        prepares gathering data for a lesson and calls gathering methods 
        """
        
        # set lesson type code for adventech.io request
        lesson_type_string = ""
        if self.lesson_type == "ad":
            lesson_type_string = ""
        else:
            if self.lesson_type == "ay":
                lesson_type_string = "-ay"
        # combine request of quarter from parameters
        request_str = ("{0}/api/v1/{1}/quarterlies/{2}-{3:02}{4}/index.json")\
            .format(self.site, self.lang_code, self.year,
                     self.quart_N, lesson_type_string)
        print("get_content by {0}".format(request_str))
        # send request to adventech.io
        r = requests.get(request_str)
        # extract from xml received in response title of lesson, description
        self.quarter_title = r.json().get('quarterly').get('title')
        self.quarter_description = r.json().get('quarterly').get('description')
        print("quarter {0}-{1:02}{2}"\
              .format(self.year, self.quart_N, lesson_type_string))
        print("*** title: {0}".format(self.quarter_title))
        # extract lessons from xml received in response 
        self.lessons_block = r.json().get('lessons')
        # enumerate lessons in lessons_block to get content from every lesson 
        for index, lesson_block in enumerate(self.lessons_block):
            lesson_block = self.lessons_block[index]
            # create new lesson and append to array of lessons
            self.lessons_set.append(lesson(lesson_block, index + 1))
            # set language of a new lesson
            self.lessons_set[-1].set_lang_code(self.lang_code)
            # call content receiving for new lesson
            self.lessons_set[-1].get_content()
        pass

    def print_quarter(self):
        """ print information about quarter, for debugging """
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
    def create_table_info(self, cursor, year, quart, name, lang):
        """ create table info in database, deprecated """
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
        """Constructor"""
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
    # array of records of quarter in xml response from adventech.io
    quarters_list_year = []
    # array of quarter objects
    quarters = []
    site = "https://sabbath-school.adventech.io"
    lang_code = "ru"
    lesson_type = 'ad'
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
        """ get list of quarters from server """
        self.quarters_list_year = []
        # create request to adventech.io from attributes
        request_str = ("{0}/api/v1/{1}/quarterlies/index.json")\
            .format(self.site, self.lang_code, self.year)
        print("get_quarters_list with {0}".format(request_str))
        # send request to server
        r = requests.get(request_str)
        # select quarters for year and append it to quarters array
        for index, quart in enumerate(r.json()):
            quart = r.json()[index]
            # select quarters for this year and not for youth
            if (int(quart.get("id").split("-")[0])
                == self.year and len(quart.get("id").split("-")) == 2):
                self.quarters_list_year.append(quart)
        print(" quarters for selected year: ")
        # sort quarters in array by quarter number
        self.quarters_list_year.sort(key = lambda quart_rec:
                                      quart_rec.get("id").split("-")[1])
        for quart in self.quarters_list_year:
            print("quarter {0}".format(quart.get("id")))
        print()
    def get_content(self):
        """ get content of year
        
        create quarter objects with appropriate parameters
        for every quarter in quarters_list_year
        and get content of every quarter """
        print("SS_year: get content")
        print("self.quarters {0}".format(self.quarters))
        # enumerate quarters elements in quarters_list_year
        for quart in self.quarters_list_year:
            print("process quarter {0}".format(quart.get("id")))
            # create new quarter object
            self.quarters.append(quarter())
            # set parameters of quarter: year and quarter number, 
            self.quarters[-1].set_quarter(self.year,
                                           int(quart.get("id").split("-")[1]))
            # set language
            self.quarters[-1].set_lang_code(self.lang_code)
            # set lesson type
            self.quarters[-1].set_lesson_type(self.lesson_type)
            # send requests chain to get content of every day
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
    SS_year_inst = SS_year()    # year class instance
    year = 0
    # name of database file
    file_name = ""
    # year in database
    db_end_year = -1
    # end quarter in database
    db_end_quart = -1
    # variable stores result of check
    # if file with name file_name is file with devotions
    db_inp_file_is_SDA_SS_devotions = False
    # last day in database
    db_last_day = 0
    def lesson_type_to_text(self):
        """ returns text description of type of lesson """
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
        """ returns default file name of database """
        file_name = "SS-{0}-{1}'{2}.devotions.SQLite3"\
            .format(self.lang_code, self.lesson_type, str(self.year)[2:4])
        return file_name
    def connect_to_db(self, file_name):
        """ opens database in file_name and check if it is actual devotions"""
        
        # check year passed in parameters
        if (self.year >= 1852 and self.year <= 2099):
            # if file name is empty then use default file name
            if (file_name == ""):
                self.file_name = self.get_def_file_name()
            else:
                self.file_name = file_name
            # check if file with file_name exists
            if (os.path.isfile(self.file_name)):
                try:
                    # try to open file_name as database
                    self.db_conn = sqlite3.connect(self.file_name)
                    self.db_cursor = self.db_conn.cursor()
                    print("connection : {0} ; cursor : {1}"\
                          .format(self.db_conn, self.db_cursor))
                    print("sqlite3 version {0}".format(sqlite3.version))
                    ret_val = 1
                except sqlite3.Error as e:
                    print(e)
                    err_name = "create database error {0}".format(e)
                    ret_val = -1
                if (ret_val == 1):
                    #process input file
                    try:
                        # check is it SDA Sabbath School devotions
                        self.db_cursor.execute("SELECT * FROM info WHERE name = 'description'")# % "description")
                        info_description = self.db_cursor.fetchall()
                        # TODO : fix check for different languages
                        if (info_description[0][1].startswith("Seventh-day Adventist Church`s Sabbath School lessons ")):
                            self.db_inp_file_is_SDA_SS_devotions = True
                            print("it is SDA Sabbath School devotion database")
                            # find the last quarter in database
                            self.db_cursor.execute("SELECT * FROM devotions WHERE devotion LIKE '<h3>%'")
                            devotion_quart_heads = self.db_cursor.fetchall()
                            for index, value in enumerate(devotion_quart_heads):
                                (self.db_end_year, self.db_end_quart) = value[1][4:10].split('-')
                                self.db_end_year = int(self.db_end_year)
                                self.db_end_quart = int(self.db_end_quart)
                            print("db_end is {0} - {1}".format(self.db_end_year, self.db_end_quart))
                            # find the last day in database
                            self.db_cursor.execute("SELECT MAX(day) FROM devotions")
                            self.db_last_day = self.db_cursor.fetchall()[0][0]
                            print("the last day in db is {0}".format(self.db_last_day))
                            if (not(self.db_end_year == self.year)):
                                ret_val = -3
                                print("year inconsistent, passed through arguments: {0}, in database of input file {1}"\
                                      .format(self.year, self.db_end_year))
                    except sqlite3.Error as e:
                        ret_val = -2
                        print("error SELECT  info from database : {0}", e)
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
        """ create new database with devotions 
        in file with name file_name if file_name not empty
        or use default file name """
        # check year
        if (self.year >= 1852 and self.year <= 2099):
            # if file_name is empty then use default file name
            if (file_name == ""):
                self.file_name = self.get_def_file_name()
            else:
                self.file_name = file_name
            print("create db with file name {0}".format(self.file_name))
            # check if file with file_name is exists
            if (not(os.path.isfile(self.file_name))):
                # create file file_name with database
                try:
                    self.db_conn = sqlite3.connect(self.file_name)
                    self.db_cursor = self.db_conn.cursor()
                    print("connection : {0} ; cursor : {1}"\
                          .format(self.db_conn, self.db_cursor))
                    print("sqlite3 version {0}".format(sqlite3.version))
                    ret_val = 1
                except sqlite3.Error as e:
                    print(e)
                    self.err_name = "create database error {0}".format(e)
                    ret_val = -1
            else:
                # if file file_name exists, then returns with error
                print("Error: file already exists")
                self.err_name = "file already exists"
                ret_val = -4
        else:
            print("set correct year 1852...2099, {0} is outside".format(self.year))
            ret_val = -5
            self.err_name = "incorrect year"
        return(ret_val)

    def get_year(self):
        """ returns list of quarters in year """
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
        
        function returns description text for database file of lesson in selected language
        it substitutes
         - the name of material - Seventh-day Adventist Church`s Sabbath School lessons
         - year and quarter
         - version: for adults or for youth
        """
        
        # set description text in different languages
        # default values is in English
        # set header of devotion
        # set description of type of lesson
        name_text = "Seventh-day Adventist Church`s Sabbath School lessons"
        if (self.lesson_type == 'ad'):
            version_text = "for adults"
        else:
            if (self.lesson_type == 'ay'):
                version_text = "for youth"
            else:
                version_text = ""
        if (self.lang_code == "ru"):
            name_text = "Пособие по изучению Библии в Субботней школе церкви Христиан адвентистов седьмого дня"
            if (self.lesson_type == 'ad'):
                version_text = "для взрослых"
            else:
                if (self.lesson_type == 'ay'):
                    version_text = "для молодёжи"
                else:
                    version_text = ""
        else:
            if (self.lang_code == "uk"):
                name_text = "Посібник з вивчення Біблії в Суботній школі церкви адвентистів сьомого дня"
                if (self.lesson_type == 'ad'):
                    version_text = "для дорослих"
                else:
                    if (self.lesson_type == 'ay'):
                        version_text = "для молоді"
                    else:
                        version_text = ""
        description_text = "{0} {1} {2}".format(name_text, version_text, self.SS_year_inst.quarters_list_year[-1].get('id'))
        return  description_text
    def get_db_detailed_info_text(self):
        """ returns detailed info in selected languages """
        themes_list = "<p> List of quarterly themes: </p>"
        if (self.lang_code == "ru"):
            themes_list = "<p> Список тем кварталов: </p>"
        if (self.lang_code == "uk"):
            themes_list = "<p> Список тем кварталів: </p>"
        for quarter in self.SS_year_inst.quarters:
            themes_list = themes_list + "<h4>" + "{0}.".format(quarter.quart_N) + " " + quarter.quarter_title + "</h4>"# + "<p>" + quarter.quarter_description + "</p>"
        from_author_of_module_text = """To send bugs and wishes on the module, use the service at <a href="https://github.com/Juzujka/SDA_SS_to_MyBible/issues"> https://github.com/Juzujka/SDA_SS_to_MyBible/issues </a>. Thanks, blessings, suggestions for help and cooperation send to juzujka@gmail.com."""
        if (self.lang_code == "ru"):
            from_author_of_module_text = """Для отправки замечаний и пожеланий по модулю воспользуйтесь сервисом по адресу <a href="https://github.com/Juzujka/SDA_SS_to_MyBible/issues">https://github.com/Juzujka/SDA_SS_to_MyBible/issues </a>. Благодарности, благословения, предложения о помощи и сотрудничестве присылайте на juzujka@gmail.com."""
        if (self.lang_code == "uk"):
            from_author_of_module_text = """Для відправки зауважень і побажань по модулю скористайтесь сервісом за адресою <a href="https://github.com/Juzujka/SDA_SS_to_MyBible/issues">https://github.com/Juzujka/SDA_SS_to_MyBible/issues </a>. Подяки, благословення, пропозиції про допомогу і співробітництво надсилайте на juzujka@gmail.com. По можливості, пишіть російською або англійською мовами."""
        detailed_info_text = "{0}<br><p>{1}</p>".format(themes_list, from_author_of_module_text)
        return detailed_info_text
    def create_table_info(self):
        """ create table 'info' for MyBible devotion database"""
        ret_val = 0
        origin_text = "'created by Egor Ibragimov, juzujka@gmail.com\n" + \
            " the text is taken from sabbath-school.adventech.io'"
        history_of_changes_text = "'2018-06-30 - created'"
        language_text = "'{0}'".format(self.lang_code)
        detailed_info_text = ""
        if self.lang_code == "ru" or self.lang_code == "uk":
            russian_numbering_text = "'{0}'".format('true')
        else:
            russian_numbering_text = "'{0}'".format('false')
        exec_string = '''CREATE TABLE IF NOT EXISTS info ( name text, value text)'''
        if DEBUG_LEVEL > 0:
            print ("execute db : {0}".format(exec_string))
        self.db_cursor.execute(exec_string)
        exec_string = '''DELETE from info'''
        if DEBUG_LEVEL > 0:
            print ("execute db : {0}".format(exec_string))
        self.db_cursor.execute(exec_string)
        exec_string = "INSERT INTO info VALUES ( 'origin', {0} )".format(origin_text)
        if DEBUG_LEVEL > 0:
            print ("execute db : {0}".format(exec_string))
        self.db_cursor.execute(exec_string)
        exec_string = """INSERT INTO info VALUES ( 'description', '{0}' )""".format(self.get_db_description_text())
        if DEBUG_LEVEL > 0:
            print ("execute db : {0}".format(exec_string))
        self.db_cursor.execute(exec_string)
        exec_string = """INSERT INTO info VALUES ( 'detailed_info', '{0}' )""".format(self.get_db_detailed_info_text())
        if DEBUG_LEVEL > 0:
            print ("execute db : {0}".format(exec_string))
        self.db_cursor.execute(exec_string)
        exec_string = "INSERT INTO info VALUES ( 'language', {0} )".format(language_text)
        if DEBUG_LEVEL > 0:
            print ("execute db : {0}".format(exec_string))
        self.db_cursor.execute(exec_string)
        exec_string = "INSERT INTO info VALUES ( 'russian_numbering', {0} )".format(russian_numbering_text)
        if DEBUG_LEVEL > 0:
            print ("execute db : {0}".format(exec_string))
        self.db_cursor.execute(exec_string)
        return(ret_val)
    def update_description(self):
        """ update description of existing database """
        exec_string = "DELETE FROM info WHERE name='description'" 
        if DEBUG_LEVEL > 0:
            print ("execute db : {0}".format(exec_string))
        self.db_cursor.execute(exec_string)
        exec_string = """INSERT INTO info VALUES ( 'description', '{0}' )""".format(self.get_db_description_text())
        if DEBUG_LEVEL > 0:
            print ("execute db : {0}".format(exec_string))
        self.db_cursor.execute(exec_string)
    def update_detailed_info(self):
        """ update detailed_info of existing database """
        exec_string = "DELETE FROM info WHERE name='detailed_info'" 
        if DEBUG_LEVEL > 0:
            print ("execute db : {0}".format(exec_string))
        self.db_cursor.execute(exec_string)
        exec_string = """INSERT INTO info VALUES ( 'detailed_info', '{0}' )""".format(self.get_db_detailed_info_text())
        if DEBUG_LEVEL > 0:
            print ("execute db : {0}".format(exec_string))
        self.db_cursor.execute(exec_string)
    def create_table_devotions(self):
        """ write days into database from gathered days in lessons in quarters in year"""
        
        exec_string = '''CREATE TABLE IF NOT EXISTS devotions (day NUMERIC, devotion TEXT)'''
        if DEBUG_LEVEL > 0:
            print ("execute db : {0}".format(exec_string))
        self.db_cursor.execute(exec_string)
        exec_string = '''CREATE UNIQUE INDEX IF NOT EXISTS devotions_index ON devotions (day ASC)'''
        if DEBUG_LEVEL > 0:
            print ("execute db : {0}".format(exec_string))
        self.db_cursor.execute(exec_string)
        days_counter = self.db_last_day + 1
        # next day after last day in database in the first day of current quarter
        lesson_counter = 1
        print("quarters len {0}".format(len(self.SS_year_inst.quarters)))
        for quarter in self.SS_year_inst.quarters:
            print("lesson_set len {0}".format(len(quarter.lessons_set)))
            for lesson in quarter.lessons_set:
                print("lesson N {0:2} - {1:2}".format(lesson_counter, lesson.lesson_N))
                print("days len {0}".format(len(lesson.days)))
                # days_accumulator concatenates html for current day
                # in the beginning and in the end of year days in database possible considers days of current quarter from year before and year after current 
                days_accumulator = ""
                for day in lesson.days:
                    # day starts from lesson number and header
                    day_content_handled = "<p>  lesson № {0} day {1}</p> <h4>{2}</h4> {3}".format(str(lesson.lesson_N), str(day.day_N), day.title, day.content)
                    if (self.lang_code == 'en'):
                        day_content_handled = "<p>  lesson № {0} day {1}</p> <h4>{2}</h4> {3}".format(str(lesson.lesson_N), str(day.day_N), day.title, day.content)
                    if (self.lang_code == 'ru'):
                        day_content_handled = "<p>  урок № {0} день {1}</p> <h4>{2}</h4> {3}".format(str(lesson.lesson_N), str(day.day_N), day.title, day.content)
                    if (self.lang_code == 'uk'):
                        day_content_handled = "<p>  урок № {0} день {1}</p> <h4>{2}</h4> {3}".format(str(lesson.lesson_N), str(day.day_N), day.title, day.content)
                    exec_string = '''INSERT INTO devotions VALUES ( ?, ? )'''
                    if DEBUG_LEVEL > 0:
                        print ("execute db : {0}".format(exec_string))
                    # if it is the first day in quarter then add quarter title and quarter description 
                    if (lesson.lesson_N == 1 and day.day_N == 1):
                        days_accumulator = "<h3>" + "{0}-{1}".format(quarter.year, quarter.quart_N) + " " + quarter.quarter_title + "</h3>" + "<p>" + quarter.quarter_description + "</p>" +  days_accumulator
                    days_accumulator = days_accumulator + day_content_handled
                    # if current day is not in current year then keep in days_accumulator
                    if (day.day_date.year == self.year):
                        # if current day is in current year then put day into database and clear days_accumulator
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
        #self.quart_N = 0
        self.err_name = ""
        self.file_name = ""
        self.db_conn = None
        self.db_cursor = None

    def __del__(self):
        self.close_db()

def adventech_ref_to_MyBible_ref(lang_code, doc, inp_tag):
    """ find bible references and convert to MyBible format"""

    # regular expression for selecting reference to book name with verses in particular book
                            #   /  book name                                         \ /    head, verse repeatable after selected book name                                                                                    \ 
    find_refs = regex.compile("(?:\d\s*)?(?:[\p{Lu}]\.\s)?[\p{Lu}]?[\p{Ll}\’\']+\.?\s*(?:\d+(?:[\:\-\,]\d+)?(?:\s*[\-\,]\s*\d+)?(?::\d+|(?:\s*[\p{Lu}]?[\p{Ll}\’\']+\s*\d+:\d+))?(?:\,\s*)?)*")

    # regular expression for selecting book name from reference with book name, head and verse
    parse_ref = regex.compile("(?:\d\s*)?(?:[\p{Lu}]\.\s)?[\p{Lu}]?[\p{Ll}\’\']+")
    
    # replacing "and" in Russian, Ukrainian, English languages to ";"
    # for simplifying handling 
    inp_tag_text = inp_tag.get_text()
    inp_tag_text = inp_tag_text.replace(" и ", "; ")
    inp_tag_text = inp_tag_text.replace(" і ", "; ")
    inp_tag_text = inp_tag_text.replace(" and ", "; ")
    inp_tag_text = inp_tag_text.replace(" und ", "; ")
    inp_tag_text = inp_tag_text.replace("–", "-")
    # replacing "'" to "’", it is similar in Ukrainian
    inp_tag_text = inp_tag_text.replace("'", "’")
    
    # collect to refs all references to Bible texts
    refs = find_refs.findall(inp_tag_text)
    if (DEBUG_LEVEL > 0):
        print("process doc {0},\n tag {1}, \n inp_tag_text {2}".format(doc, inp_tag, inp_tag_text))
        print("find_refs {0}".format(refs))
        print(" * references: *")

    # insert ";" between references, do not insert in the end
    is_last_ref = True  #mark: it is the end reference, beginning from the end 
    
    # process references from end to beginning
    # to not to process result of processing
    for ref in reversed(refs):
        book_name_parse_ref = parse_ref.match(ref)
        book_name_parse_ref_group = book_name_parse_ref.group()
        book_name = book_name_parse_ref_group.replace(" ", "")
        book_N = bible_codes.book_index_to_MyBible[lang_code].get(book_name)
        if (book_N == None):
            print("! referense not recognised, refs : {0} ; ref {1}; book name {2}".format(refs, ref, book_name))
            #print("doc: {0}".format(doc))
        if (DEBUG_LEVEL > 0):
            print("ref: {0} parsed is {1} name is {2}, N is {3}".format(ref, parse_ref.match(ref), book_name, book_N))
        numeric_part = (ref[parse_ref.match(ref).span()[1] + 1:]).replace(" ", "")
        # concatenate reference from reference header "B:",
        # book number and head number with verse number 
        if (book_N == 380 or book_N == 700 or book_N == 710 or book_N == 720 or book_N == 640):
            # if book Obadiah or 2 John or 3 John or Jude or Philemon,
            # which has one head then add to the reference head one "1:"
            MyBible_ref = "B:{0} 1:{1}".format(book_N, numeric_part)
        else:
            MyBible_ref = "B:{0} {1}".format(book_N, numeric_part)
        if (DEBUG_LEVEL > 0):
            print("MyBible ref: {0}".format(MyBible_ref))
        MyBible_a_tag = doc.new_tag("a", href=MyBible_ref)
        MyBible_a_tag.insert(0, "{0}.{1}".format(book_name, numeric_part))
        
        # add ; between references
        if not(is_last_ref):
            inp_tag.insert_after("; ")
        inp_tag.insert_after(MyBible_a_tag)
        is_last_ref = False
    inp_tag.decompose()

        
def adventech_lesson_to_MyBibe_lesson(doc, lang_code):
    """ convert lesson to MyBible format

     parces lesson material,
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
    parser.add_argument("-y", "--year",     type = int, help="year for lessons", default = -1)
    parser.add_argument("-a", "--append",   action = "store_true", help = "add new lessons to the end of existing database", default = False)
    parser.add_argument("-o", "--db_file",  help = "name of database output file", default = "")
    parser.add_argument("-l", "--list",     action = "store_true", help = "get list of available quarters", default = False)
    parser.add_argument(      "--lang",     action = "store",      help = "language", default = "ru")
    parser.add_argument(      "--type",     action = "store",      help = "type of lesson: ad - adult, ay - youth", default = "ad")
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
