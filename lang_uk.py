#! /usr/bin/env python3
# encoding: utf-8

""" Convert book of Bible abbreviation to MyBible book of Bible number'
 
 This module considers dictionary of
 pairs of variants of books of Bible abbreviations
 with its number in MyBible format.
 
"""

db_info_description_title = "Посібник з вивчення Біблії в Суботній школі церкви адвентистів сьомого дня"
db_info_description_version_adult = "для дорослих"
db_info_description_version_youth = "для молоді"
db_info_description_list_of_quarterly_themes = "Список тем кварталів:"
db_info_description_from_author = """Для відправки зауважень і побажань по модулю скористайтесь сервісом за адресою <a href="https://github.com/Juzujka/SDA_SS_to_MyBible/issues">https://github.com/Juzujka/SDA_SS_to_MyBible/issues </a>. Подяки, благословення, пропозиції про допомогу і співробітництво надсилайте на juzujka@gmail.com. По можливості, пишіть російською або англійською мовами."""
db_info_description_origin_text = """created by Egor Ibragimov, juzujka@gmail.com\nthe text is taken from sabbath-school.adventech.io"""
db_info_description_lesson = "урок"
db_info_description_day = "день"

def ref_tag_preprocess(inp_tag_text):
    """adopting references in lessons in Ukrainian"""

    # some words in references
    inp_tag_text = inp_tag_text.replace("до римлян", "Римл")
    inp_tag_text = inp_tag_text.replace(" и ", "; ")
    inp_tag_text = inp_tag_text.replace(" і ", "; ")
    inp_tag_text = inp_tag_text.replace("–", "-")
    # replacing "'" to "’", it is similar in Ukrainian
    inp_tag_text = inp_tag_text.replace("'", "’")
    return inp_tag_text

book_index_to_MyBible = dict([\
('Бут',10),\
('Вих',20),\
('Лев',30),\
('Левит',30),\
('Чис',40),\
('Числ',40),\
('Числа',40),\
('П.Зак',50),\
('І.Нав',60),\
('Суд',70),\
('Рут',80),\
('1Сам',90),\
('2Сам',100),\
('1Цар',110),\
('2Цар',120),\
('1Хронік',130),\
('2Хронік',140),\
('Єздр',150),\
('Езд',150),\
('Ездр',150),\
('Ездри',150),\
('Неєм',160),\
('Неем',160),\
('Ест',190),\
('Естер',190),\
('Йов',220),\
('Йова',220),\
('Псал',230),\
('Прит',240),\
('Прип',240),\
('Екк',250),\
('Екл',250),\
('П.Пісн',260),\
('Ісаї',290),\
('Єрем',300),\
('Пл.Єр',310),\
('Єзек',330),\
('Дан',340),\
('Даниїла',340),\
('Осії',350),\
('Йоїла',360),\
('Йоіла',360),\
('Амоса',370),\
('Овд',380),\
('Йони',390),\
('Міх',400),\
('Мих',400),\
('Михея',400),\
('Наума',410),\
('Авак',420),\
('Соф',430),\
('Огія',440),\
('Зах',450),\
('Зак',450),\
('Мал',460),\
('Матв',470),\
('Матвія',470),\
('Мрк',480),\
('Марка',480),\
('Луки',490),\
('Івана',500),\
('Дії',510),\
('Якова',660),\
('1Петра',670),\
('2Петра',680),\
('1Івана',690),\
('2Івана',700),\
('3Івана',710),\
('Юди',720),\
('Римл',520),\
('1Кор',530),\
('2Кор',540),\
('Гал',550),\
('Ефес',560),\
('Филп',570),\
('Колос',580),\
('1Сол',590),\
('2Сол',600),\
('1Тим',610),\
('2Тим',620),\
('Тита',630),\
('Тит',630),\
('Филм',640),\
('Євр',650),\
('Об’явл',730),\
('Об’явлення',730),\
])
