#! /usr/bin/env python3
# encoding: utf-8
import requests
from bs4 import BeautifulSoup
#import uno
import bible_codes
import re
import sqlite3
import datetime
from _datetime import timedelta
#from asn1crypto.core import Integer

DEBUG_LEVEL = 0


class text_material:
    """some text material: text for a day, intro, comments"""
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
    """day of lesson"""
    day_N = 0
    day_data = 0
    full_path = ""
    content = ""
    title = ""
    def get_content(self, full_path, day_N):
        self.full_path = full_path
        self.day_N = day_N
        request_str = ("{0}/days/{1:02}/read/index.json")\
            .format(self.full_path, self.day_N)
        # print("request is {0}".format(request_str))
        r = requests.get(request_str)
        # print("lesson keys: {0}".format(r.json().keys()))
        # print("lesson content: {0}".format(r.json().get('content')))
        # for item in r.json().get('lessons'):
        #    print (item)
        #    print(type(item)) 
        # r = requests.get('https://sabbath-school.adventech.io/api/v1/languages/index.json')
        # print(r.json())
        self.content = r.json().get('content')
        self.content = adventech_lesson_to_MyBibe_lesson(self.content)
        self.day_data = datetime.datetime.strptime(r.json().get('date'), "%d/%m/%Y")
        self.title = r.json().get('title')
    def __init__(self, day_N):
        self.day_N = day_N

class comment(text_material):
    """comment for lesson, for class leaders"""

    def get_content(self, lesson):
        pass


class lesson:
    """lesson"""
    lesson_N = 0
    lesson_title = ""
    lesson_start = datetime.date(2000, 1, 1)
    lesson_end = datetime.date(2000, 1, 1)
    lesson_full_path = ""
    lesson_index = ""
    days = []

    def get_lesson_N(self, lesson_block):
        # print("lesson id {0}".format(lesson_block.get("id")))
        return lesson_block.get("id")

    def get_lesson_start(self, lesson_block):
        start_string = lesson_block.get("start_date")
        # print("start_string {0}".format(start_string))
        return datetime.date(int(start_string.split('/')[2]), \
                                                 int(start_string.split('/')[1]), \
                                                 int(start_string.split('/')[0]))

    def get_lesson_end(self, lesson_block):
        end_string = lesson_block.get("end_date")
        # print("end_string {0}".format(start_string))
        return datetime.date(int(end_string.split('/')[2]), \
                                                 int(end_string.split('/')[1]), \
                                                 int(end_string.split('/')[0]))

    def get_lesson_full_path(self, lesson_block):
        return lesson_block.get("full_path")

    def get_lesson_index(self, lesson_block):
        return    lesson_block.get("index")

    def get_lesson_title(self, lesson_block):
        # print("lesson title {0}".format(lesson_block.get("title")))
        return lesson_block.get("title")

    def get_lesson_content(self, lesson_block):
        pass

    def get_content(self, lesson_block):
        self.lesson_N = int(self.get_lesson_N(lesson_block))
        self.lesson_title = self.get_lesson_title(lesson_block)
        self.lesson_start = self.get_lesson_start(lesson_block)
        self.lesson_end = self.get_lesson_end    (lesson_block)
        self.lesson_full_path = self.get_lesson_full_path (lesson_block)
        self.lesson_index = self.get_lesson_index(lesson_block)
        day_text_accumulator = ""
        for day_N in range(1, 8):
        #for day_N in range(1, 3):
            print("day {0} add to array of {1}".format(day_N, len(self.days)))
            curr_day = day(day_N)
            print("day date is {0}".format(curr_day.day_data))
            self.days.append(curr_day)
            self.days[-1].get_content(self.lesson_full_path, day_N)
            #self.days[-1].content = "<p> {0} : {1}</p> {2}".format(str(self.lesson_start + timedelta(day_N-1)), self.days[-1].title, self.days[-1].content)
        # self.day.get_content(lesson)
        pass

    def print_content(self):
        pass
    def __init__(self, lesson_N):
        self.lesson_N = lesson_N
        self.lesson_title = ""
        self.days = []
        print("create lesson {0}, days is {1}".format(self.lesson_N, len(self.days)))
        

class quarter:
    """quarter, includes lessons"""
    """self.site = "https://sabbath-school.adventech.io"
    self.year = 0
    self.quart_N = 0
    self.lang_code = "ru"
    intro()
    self.lessons_block = None
    self.lessons_set = []
    self.quarter_title = "" """

    def set_quarter(self, year, quarter):
        self.year = year
        self.quart_N = quarter

    def set_db_cursor(self, db_cursor):
        self.db_cursor = db_cursor

    def get_content(self):
        request_str = ("{0}/api/v1/{1}/quarterlies/{2}-{3:02}/index.json")\
            .format(self.site, self.lang_code, self.year, self.quart_N)
        r = requests.get(request_str)
        self.quarter_title = r.json().get('quarterly').get('title')
        self.quarter_description = r.json().get('quarterly').get('description')
        print("*** title : {0}".format(self.quarter_title))
        print("*** description : {0}".format(self.quarter_description))
        self.quarter_title = r.json().get('quarterly').get('title')
        self.lessons_block = r.json().get('lessons')
        # print("lessons_block {0}".format(self.lessons_block))
        print("lesson_set {0}".format(self.lessons_set))
        #for index in range(0, 2):
        for index, lesson_block in enumerate(self.lessons_block):
            lesson_block = self.lessons_block[index]
            self.lessons_set.append(lesson(index + 1))
            self.lessons_set[-1].get_content(lesson_block)
            print("appended {0}".format(lesson_block))
            # print("lesson N is {0}".format(self.lessons_set[-1].lesson_N))
            # print("lesson title is {0}".format(self.lessons_set[-1].lesson_title))
        print("lesson_set size {0}".format(len(self.lessons_set)))
        pass

    #def build_quarter(self):
    #    self.get_content()
    #    pass

    def print_quarter(self):
        for index, lesson_item in enumerate(self.lessons_set):
            print("lesson_set[{0}] {1}".format(index, self.lessons_set[index].lesson_N))
            print("lesson_set[{0}] {1}".format(index, self.lessons_set[index].lesson_title))
            print("lesson_set[{0}] {1}".format(index, self.lessons_set[index].lesson_start))
            print("lesson_set[{0}] {1}".format(index, self.lessons_set[index].lesson_end))
            print("lesson_set[{0}] {1}".format(index, self.lessons_set[index].lesson_full_path))
            print("lesson_set[{0}] {1}".format(index, self.lessons_set[index].lesson_index))
            for day in self.lessons_set[index].days:
                print("day {0} is {1}".format(day.day_N, day.content))
        
    def create_table_info(self, cursor, year, quart, name, lang):
        ret_val = 0
        origin_text = "'created by Egor Ibragimov, juzujka@gmail.com\n" + \
            " the text is taken from sabbath-school.adventech.io'"
        history_of_changes_text = "'2018-06-30 - created'"
        language_text = "'{0}'".format(lang)
        description_text = "'Seventh Day Adventist Cheurch`s Sabbath School lesson {0}-{1}'".format(year, quart)
        detailed_info_text = ""
        # exec_string = "CREATE TABLE 'info' (origin TEXT, {0} TEXT, history_of_changes TEXT, {1} TEXT, language TEXT, {2} TEXT)".format(origin_text, history_of_changes_text, language_text)
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
        #intro = intro()
        self.lessons_block = None
        self.lessons_set = []
        self.quarter_title = ""
        self.quarter_description = ""
        self.db_cursor = None
        pass

class SS_year:
    quarters_list_whole = []
    quarters_list_year = []
    quarters = []
    site = "https://sabbath-school.adventech.io"
    lang_code = "ru"
    def set_year(self, year):
        self.year = year
    def get_quarters_list(self):
        self.quarters_list = []
        request_str = ("{0}/api/v1/{1}/quarterlies/index.json")\
            .format(self.site, self.lang_code, self.year)
        r = requests.get(request_str)
        #print("*** quarterlies : {0}".format(r.json()))
        #for index in range(0, 2):
        #for index, lesson_block in enumerate(self.lessons_block):
        #    lesson_block = self.lessons_block[index]
        for index, quart in enumerate(r.json()):
        #for index in range(0, 1):
        #for quart in r.json():
            quart = r.json()[index]
            # select quarters for this year and not for youth
            if (int(quart.get("id").split("-")[0]) == self.year and len(quart.get("id").split("-")) == 2):
                self.quarters_list_year.append(quart)
        print(" quartrers for selected year")
        self.quarters_list_year.sort(key = lambda quart_rec : quart_rec.get("id").split("-")[1])
        for quart in self.quarters_list_year:
            print("{0} {1}".format(quart.get("id"), quart))
        print()
    def get_content(self):
        self.get_quarters_list()
        print("SS_year: get content")
        for quart in self.quarters_list_year:
            print("{0} {1}".format(quart.get("id"), quart))
            self.quarters.append(quarter())
            #self.quarters[-1].set_db_cursor(self.db_cursor)
            self.quarters[-1].set_quarter(self.year, int(quart.get("id").split("-")[1]))
            self.quarters[-1].get_content()

        
    def __init__(self):
        self.year = 0
        self.site = "https://sabbath-school.adventech.io"
        self.lang_code = "ru"
        self.quarters_list_whole = []
        self.quarters_list_year = []
        self.quarters = []

class db_MyBible_devotions_SS:
    lang = 'ru'
    SS_year_inst = SS_year()
    year = 0
    def set_year(self, year):
        self.year = year
        self.SS_year_inst.set_year(self.year)
    #def set_quarter(self, year, quart_N):
    #    self.year = year
    #    self.quart_N = quart_N

        # self.err_name = ""
        # self.file_name = ""
        # self.db_conn = None
        # self.db_cursor = None
    def create_db(self):
        if (self.year >= 1888 and self.year <= 2099):
            #if (self.quart_N >= 1 and self.quart_N <= 4):
            #    self.file_name = "SDA-SS-{0}-{1}.devotions.SQLite3".format(self.year, self.quart_N)
            self.file_name = "SDA-SS-{0}.devotions.SQLite3".format(self.year)
            print("create db with file name {0}".format(self.file_name))
            try:
                self.db_conn = sqlite3.connect(self.file_name)
                self.db_cursor = self.db_conn.cursor()
                print("connection : {0} ; cursor : {1}".format(self.db_conn, self.db_cursor))
                print("sqlite3 version {0}".format(sqlite3.version))
                ret_val = 1
            except sqlite3.Error as e:
                print(e)
                err_name = "create database error {0}".format(e)
                ret_val = -1
            #else:
            #    print("set correct quarter number 1...4, {0} is outside".format(self.quart_N))
            #    err_name = "incorrect quarter number"
        else:
            print("set correct year 1888...2099, {0} is outside".format(self.year))
            self.err_name = "incorrect year"

    def x_get_quarter(self):
        self.quarter = quarter()
        self.quarter.set_db_cursor(self.db_cursor)
        self.quarter.set_quarter(self.year, self.quart_N)
        self.quarter.get_content()()
    def get_year(self):
        self.SS_year_inst.set_year(self.year)
        self.SS_year_inst.get_quarters_list()
    def get_content(self):
        self.SS_year_inst.get_content()
    def create_table_info(self):
        ret_val = 0
        origin_text = "'created by Egor Ibragimov, juzujka@gmail.com\n" + \
            " the text is taken from sabbath-school.adventech.io'"
        history_of_changes_text = "'2018-06-30 - created'"
        language_text = "'{0}'".format(self.lang)
        description_text = "'Seventh Day Adventist Church`s Sabbath School lessons {0}'".format(self.year)
        detailed_info_text = ""
        # exec_string = "CREATE TABLE 'info' (origin TEXT, {0} TEXT, history_of_changes TEXT, {1} TEXT, language TEXT, {2} TEXT)".format(origin_text, history_of_changes_text, language_text)
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
        exec_string = """INSERT INTO info VALUES ( 'description', {0} )""".format(description_text)
        if DEBUG_LEVEL > 0:
            print ("execute db : {0}".format(exec_string))
        self.db_cursor.execute(exec_string)
        exec_string = "INSERT INTO info VALUES ( 'language', {0} )".format(language_text)
        if DEBUG_LEVEL > 0:
            print ("execute db : {0}".format(exec_string))
        self.db_cursor.execute(exec_string)
        return(ret_val)

    def create_table_devotions(self):
        exec_string = '''CREATE TABLE IF NOT EXISTS devotions (day NUMERIC, devotion TEXT)'''
        if DEBUG_LEVEL > 0:
            print ("execute db : {0}".format(exec_string))
        self.db_cursor.execute(exec_string)
        exec_string = '''DELETE from devotions'''
        if DEBUG_LEVEL > 0:
            print ("execute db : {0}".format(exec_string))
        self.db_cursor.execute(exec_string)
        exec_string = '''CREATE UNIQUE INDEX IF NOT EXISTS devotions_index ON devotions (day ASC)'''
        if DEBUG_LEVEL > 0:
            print ("execute db : {0}".format(exec_string))
        self.db_cursor.execute(exec_string)
        days_counter = 1
        lesson_counter = 1
        print("quarters len {0}".format(len(self.SS_year_inst.quarters)))
        for quarter in self.SS_year_inst.quarters:
            print("lesson_set len {0}".format(len(quarter.lessons_set)))
            for lesson in quarter.lessons_set:
                print("lesson N {0:2} - {1:2}".format(lesson_counter, lesson.lesson_N))
                print("days len {0}".format(len(lesson.days)))
                days_accumulator = ""
                for day in lesson.days:
                    #day_content_handled = "<p> {0} : {1}</p> {2}".format(str(lesson.lesson_start + timedelta(day.day_N-1)), day.title, day.content) 
                    day_content_handled = "<p>  урок № {0} день {1}</p> <h4>{2}</h4> {3}".format(str(lesson.lesson_N), str(day.day_N), day.title, day.content)
                    exec_string = '''INSERT INTO devotions VALUES ( ?, ? )'''
                    if DEBUG_LEVEL > 0:
                        print ("execute db : {0}".format(exec_string))
                    #print("day.content: {0}".format(day.content))
                    if (lesson.lesson_N == 1 and day.day_N == 1):
                        days_accumulator = "<h3>" + "{0}-{1}".format(quarter.year, quarter.quart_N) + " " + quarter.quarter_title + "</h3>" + "<p>" + quarter.quarter_description + "</p>" +  days_accumulator
                    days_accumulator = days_accumulator + day_content_handled
                    if (day.day_data.year == self.year):
                        print( "put day {0}: ".format(days_counter))
                        #print(days_accumulator)
                        self.db_cursor.execute(exec_string, (days_counter, days_accumulator))
                        days_accumulator = ""
                        days_counter += 1
                    else:
                        print("move the day {0} to the next day".format(day.day_data))
                        #days_accumulator = days_accumulator + day_content_handled
                lesson_counter += 1
        pass
    def close_db(self):
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


def find_lang(lang_name):

    r = requests.get('https://sabbath-school.adventech.io/api/v1/languages/index.json')
    # print(r.json())
    # print(r.json()[1], "type is ", type(r.json()[1]))

    # print(r.json().keys())

    lang_code = ""
    print("r.json(): {0}".format(r.json()))
    print("type or r.json(): {0}".format(type(r.json())))
    for item in r.json():
        # print("item {0} key {1}".format(item, item.get('name')))
        print("item: {0}", format(item))
        print("type(item): {0}", format(type(item)))
        if (item.get('name') == lang_name):
            lang_code = item.get('code')

    # print ("code of {0} is {1}".format(lang_name, lang_code))

    return lang_code

# find code for Russian language


def get_lessons_list(lang_code, lessons_year, lessons_quarter):
    request_str = ("https://sabbath-school.adventech.io/api/v1/{0}/quarterlies/{1}-{2:02}/index.json")\
        .format(lang_code, lesson_year, lesson_quarter)
    # print("request is {0}".format(request_str))
    r = requests.get(request_str)
    # print ("items: {0}".format(r.json()))
    print("*** title : {0}".format(r.json().get('quarterly').get('title')))
    # print ("items: {0}".format(r.json().get('quarterly')))
    # print ("quarterly.description : {0}".format(r.json().get('quarterly').get('description')))
    # print ("--lessons--")
    # for item in r.json().get('lessons'):
    #    print (item)
    #    print(type(item))
    lessons = {'title':r.json().get('quarterly').get('title'), 'list':r.json().get('lessons')}
    # lessons['title'] = r.json().get('title')
    # lessons['list'] = r.json().get('lessons')
    return(lessons)


def get_lesson(lang_code, lesson_year, lesson_quarter, lesson_N, lesson_day):
    request_str = ("https://sabbath-school.adventech.io/api/v1/{0}/quarterlies/{1}-{2:02}/lessons/{3:02}/days/{4:02}/read/index.json")\
        .format(lang_code, lesson_year, lesson_quarter, lesson_N, lesson_day)
    # print("request is {0}".format(request_str))
    r = requests.get(request_str)
    # print("lesson keys: {0}".format(r.json().keys()))
    # print("lesson content: {0}".format(r.json().get('content')))
    # for item in r.json().get('lessons'):
    #    print (item)
    #    print(type(item)) 
    # r = requests.get('https://sabbath-school.adventech.io/api/v1/languages/index.json')
    # print(r.json())
    return(r.json().get('content'))


def adventech_ref_to_MyBible_ref(doc, inp_tag):
    # print("ru_to_MyBible keys : {0}".format(bible_codes.ru_to_MyBible.keys()))
    # print("ru_to_MyBible : {0}".format(bible_codes.ru_to_MyBible.get('Быт')))
    # out_text = inp_tag
    # find_book_name = re.search('{1,0}?{А,я}*', out_text)
    # find_book_name = re.compile('[А-я]*.[0-9]*')
    find_refs = re.compile('(?:\d\s*)?[А-Я]?[а-я]+\.?\s*\d+(?:[:-]\d+)?(?:\s*-\s*\d+)?(?::\d+|(?:\s*[А-Я]?[а-я]+\s*\d+:\d+))?')
    parse_ref = re.compile('(\d?\s?[А-Я]?[а-я]+)')
    inp_tag_text = inp_tag.get_text()
    inp_tag_text = inp_tag_text.replace(" и ", "; ")
    refs = find_refs.findall(inp_tag_text)
    if (DEBUG_LEVEL > 0):
        print("process doc {0},\n tag {1}, \n inp_tag_text {2}".format(doc, inp_tag, inp_tag_text))
        print("find_refs {0}".format(refs))
        print(" * references: *")
    for ref in reversed(refs):
        book_name = parse_ref.match(ref).group().replace(" ", "")
        book_N = bible_codes.ru_to_MyBible.get(book_name)
        if (book_N == None):
            print("! referense not recognised:{0}".format(refs))
        if (DEBUG_LEVEL > 0):
            print("ref: {0} parsed is {1} name is {2}, N is {3}".format(ref, parse_ref.match(ref), book_name, book_N))
        numeric_part = (ref[parse_ref.match(ref).span()[1] + 1:]).replace(" ", "")
        MyBible_ref = "B:{0} {1}".format(book_N, numeric_part)
        if (DEBUG_LEVEL > 0):
            print("MyBible ref: {0}".format(MyBible_ref))
        MyBible_a_tag = doc.new_tag("a", href=MyBible_ref)
        MyBible_a_tag.insert(0, "{0}.{1}".format(book_name, numeric_part))
        inp_tag.insert_after(MyBible_a_tag)
    inp_tag.decompose()

        
def adventech_lesson_to_MyBibe_lesson(doc):
    ret_val = 0
    doc_soup = BeautifulSoup(doc, 'html.parser')
    if (DEBUG_LEVEL > 0):
        print ('anchors')
    anchors = doc_soup.find_all('a', class_='verse')
    #anchors = doc_soup.find_all('a', class_='biem')

    for item in list(anchors):
        if (DEBUG_LEVEL > 0):
            print("item")
            print(item)
        bible_verses = item.get_text()
        if (DEBUG_LEVEL > 0):
            print("bible verses: {0}".format(bible_verses))
        adventech_ref_to_MyBible_ref(doc_soup, item)
        # replacing_verse = lesson_01_soup.new_tag("a", href='B:10 1:31')
        # replacing_verse.insert(0, '1:31')
        # item.insert_after(replacing_verse)
        # item.decompose()
    doc = str(doc_soup)
    #print("doc after link conversion : {0}".format(doc))
    ret_val = 1
    return(doc)
    
    # print("re finds: {0}".format(find_book_name.findall(out_text)))


def db_connection_create(db_file):
    """ create a database connection to a SQLite database """
    ret_val = 0
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        print("connection : {0} ; cursor : {1}".format(connection, cursor))
        print("sqlite3 version {0}".format(sqlite3.version))
        ret_val = 1
    except sqlite3.Error as e:
        print(e)
        ret_val = -1
    return({'conn':connection, 'cursor':cursor})


def db_connection_close(connection):
    connection.commit()
    connection.close()


def module_create_table_info(cursor, year, quart, name, lang):
    ret_val = 0
    origin_text = "'created by Egor Ibragimov, juzujka@gmail.com\n" + \
        " the text is taken from sabbath-school.adventech.io'"
    history_of_changes_text = "'2018-06-30 - created'"
    language_text = "'{0}'".format(lang)
    description_text = "'Seventh Day Adventist Cheurch`s Sabbath School lesson {0}-{1}'".format(year, quart)
    # exec_string = "CREATE TABLE 'info' (origin TEXT, {0} TEXT, history_of_changes TEXT, {1} TEXT, language TEXT, {2} TEXT)".format(origin_text, history_of_changes_text, language_text)
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
# print("code of {0} is {1}".format(lang_name, find_lang(lang_name)))
if __name__ == '__main__':
    lang_name = "Russian"
    lesson_year = 2018
    lesson_quarter = 2
    #SS_inst = SS_year(lesson_year)
    #test_text_1 = """ <html><head><title>Page title</title></head><body><p>Прочитайте <a href="/beta/bref/43:5:39;14:6;20:31" data-biem="bt-2d8c19c" class="biem">Ин. 5:39; 14:6 и 20:31</a>. Библия, в частности, Евангелие, дает нам самую надежную информацию об Иисусе. Что эти конкретные тексты в Евангелии от Иоанна сообщают нам о Спасителе? Почему Христос так важен для нас и нашей веры?  Мы изучаем Слово Божье, ибо это высший источник истины. Иисус есть Истина, и в Библии мы открываем для себя Иисуса. Здесь, в Божьем Слове, Ветхом и Новом Заветах, мы узнаем, Кто есть Иисус и что Он совершил для нас. Затем мы проникаемся к Нему любовью и вверяем Ему наши жизнь и душу. Следуя за Иисусом и повинуясь Его наставлениям, открытым в Его Слове, мы можем освободиться от уз греха и этого мира. «Итак, если Сын освободит вас, то истинно свободны будете» (<a href="/beta/bref/43:8:36" data-biem="bt-1dd7f30" class="biem">Ин. 8:36</a>).</p> </body></html>"""
    #adventech_lesson_to_MyBibe_lesson(test_text_1)
    
    
    #SS_inst.get_content()
    devotions = db_MyBible_devotions_SS()
    devotions.set_year(lesson_year)
    #devotions.set_quarter(lesson_year, lesson_quarter)
    devotions.create_db()
    #devotions.get_quarter()
    #devotions.quarter.print_quarter()
    devotions.SS_year_inst.get_content()
    print ("-- create_table_info --")
    devotions.create_table_info()
    print ("-- create_table_devotions --")
    devotions.create_table_devotions()
    
    
    """
    lessons_list = get_lessons_list('ru', 2018, 2)
    print("quarter title: {0}".format(lessons_list['title']))
    for item in lessons_list['list']:
        print ("id: {0}, title: {1}".format(item.get("id"), item.get("title")))

    db_file_name = "SDA_SS_{0}_{1}_ru.devotions.sqlite3".format(lesson_year, lesson_quarter)
    print("DB file name : {0}".format(db_file_name))
    db_conn = None
    db_cursor = None
    db_conn = db_connection_create(db_file_name)
    
    
    
    lesson_01 = get_lesson('ru', 2018, 2, 1, 1)
    #print(lesson_01)
    lesson_01_soup = BeautifulSoup(lesson_01, 'html.parser')

    #print(lesson_01_soup.prettify())

    adventech_lesson_to_MyBibe_lesson(lesson_01_soup)
        
    #print("after handling")
    #print(lesson_01_soup.prettify())
    module_create_table_info(db_conn['cursor'], lesson_year, lesson_quarter, "lesson_name", "ru")
    
    db_connection_close(db_conn['conn'])
    """
