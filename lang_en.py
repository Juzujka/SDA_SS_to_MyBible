#! /usr/bin/env python3
# encoding: utf-8

""" Convert book of Bible abbreviation to MyBible book of Bible number'
 
 This module considers dictionary of
 pairs of variants of books of Bible abbreviations
 with its number in MyBible format.
 
 Dictionaries are collected in array which indexed by language code.
 on 2019/03 available languages are
 - Russian
 - English
 - Ukrainian 
"""

db_info_description = {\
    "en":"Seventh-day Adventist Church`s Sabbath School lessons",
    }
db_info_description_version_adult = {\
    "en":"for adults",
    }
db_info_description_version_youth = {\
    "en":"for youth",
    }
list_of_quarterly_themes = {\
    "en":"List of quarterly themes:",
    }
from_author = {\
    "en":"""To send bugs and wishes on the module, use the service at <a href="https://github.com/Juzujka/SDA_SS_to_MyBible/issues"> https://github.com/Juzujka/SDA_SS_to_MyBible/issues </a>. Thanks, blessings, suggestions for help and cooperation send to juzujka@gmail.com.""",\
    }
origin_text = {\
    "en":"""created by Egor Ibragimov, juzujka@gmail.com\nthe text is taken from sabbath-school.adventech.io""",\
    }
lesson = {\
    "en":"lesson",\
    }
day = {\
    "en":"day",\
    }

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
    for i1, (key, val) in enumerate(book_index_to_MyBible['en'].items()):
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
    inp_tag_text = inp_tag_text.replace(" and ", "; ")
    inp_tag_text = inp_tag_text.replace("–", "-")
    inp_tag_text = inp_tag_text.replace("to", "-")
    # replacing "'" to "’", it is similar in Ukrainian
    return inp_tag_text


ref_tag_preprocess = {
    'en':ref_tag_preprocess_en,
     }


book_index_to_MyBible = {}

book_index_to_MyBible['en'] = dict([\
('Gen',10),\
('Genesis',10),\
('Exo',20),\
('Exod',20),\
('Exodus',20),\
('Lev',30),\
('Leviticus',30),\
('Num',40),\
('number',40),\
('Numbers',40),\
('Deu',50),\
('Deut',50),\
('Deuteronomy',50),\
('Josh',60),\
('Joshua',60),\
('Judg',70),\
('Judges',70),\
('Ruth',80),\
('1Sam',90),\
('1Samuel',90),\
('2Sam',100),\
('2Samuel',100),\
('1Kin',110),\
('1King',110),\
('1Kings',110),\
('2Kin',120),\
('2King',120),\
('2Kings',120),\
('1Chr',130),\
('1Chron',130),\
('1Chronicles',130),\
('2Chr',140),\
('2Chron',140),\
('2Chronicles',140),\
('Ezr',150),\
('Ezra',150),\
('Neh',160),\
('Nehemiah',160),\
('Esth',190),\
('Esther',190),\
('Job',220),\
('Ps',230),\
('Psalm',230),\
('Prov',240),\
('Proverbs',240),\
('Eccl',250),\
('Eccles',250),\
('Ecclesiastes',250),\
('Song',260),\
('Songs',260),\
('Sol',260),\
('Isa',290),\
('Isaiah',290),\
('Jer',300),\
('Jeremiah',300),\
('Lam',310),\
('Lamentations',310),\
('Ezek',330),\
('Ezekiel',330),\
('Dan',340),\
('Daniel',340),\
('Hos',350),\
('Hosea',350),\
('Joel',360),\
('Am',370),\
('Amos',370),\
('Oba',380),\
('Obadiah',380),\
('Jona',390),\
('Jonah',390),\
('Mic',400),\
('Micah',400),\
('Nah',410),\
('Nahum',410),\
('Hab',420),\
('Habakkuk',420),\
('Zeph',430),\
('Zephaniah',430),\
('Hag',440),\
('Haggai',440),\
('Zech',450),\
('Zechariah',450),\
('Mal',460),\
('Malachi',460),\
('Mat',470),\
('Matt',470),\
('Matthew',470),\
('Mar',480),\
('Mark',480),\
('Luk',490),\
('Luke',490),\
('John',500),\
('Acts',510),\
('Jam',660),\
('James',660),\
('1Peter',670),\
('1Pet',670),\
('2Pet',680),\
('2Peter',680),\
('1Jn',690),\
('1John',690),\
('2Jn',700),\
('2John',700),\
('3Jn',710),\
('3John',710),\
('Rom',520),\
('Romans',520),\
('1Cor',530),\
('1Corinthians',530),\
('2Cor',540),\
('2Corinthians',540),\
('Gal',550),\
('Galatians',550),\
('Eph',560),\
('Ephesians',560),\
('Phil',570),\
#('Philem',570),\
('Philippians',570),\
('Col',580),\
('Colossians',580),\
('1Ths',590),\
('1Thess',590),\
('1Thessalonians',590),\
('2Ths',600),\
('2Thess',600),\
('2Thessalonians',600),\
('1Tim',610),\
('1Timothy',610),\
('2Tim',620),\
('2Timothy',620),\
('Tit',630),\
('Titus',630),\
('Phlm',640),\
('Heb',650),\
('Hebrews',650),\
('Jude',720),\
('Rev',730),\
('Revelation',730),\
])

