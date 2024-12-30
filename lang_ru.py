#! /usr/bin/env python3
# encoding: utf-8

""" Internationalization for Russian
 
 This module considers dictionary of
 pairs of variants of books of Bible abbreviations
 with its number in MyBible format, function for preprocessing references from text materials to the common format,
 and some text for internationalization.
 
"""
import regex as re

db_info_description_title = "Пособие по изучению Библии в Субботней школе церкви Христиан адвентистов седьмого дня"
db_info_description_version_adult = "для взрослых"
db_info_description_version_youth = "для молодёжи"
db_info_description_list_of_quarterly_themes = "Список тем кварталов:"
db_info_description_from_author = """Для отправки замечаний и пожеланий по модулю воспользуйтесь сервисом по адресу <a href="https://github.com/Juzujka/SDA_SS_to_MyBible/issues">https://github.com/Juzujka/SDA_SS_to_MyBible/issues </a>. Благодарности, благословения, предложения о помощи и сотрудничестве присылайте на juzujka@gmail.com."""
db_info_description_origin_text = """created by Egor Ibragimov, juzujka@gmail.com\nthe text is taken from sabbath-school.adventech.io"""
db_info_description_lesson = "урок"
db_info_description_day = "день"

def ref_tag_preprocess(inp_tag_text):
    """adopting references in lessons in Russian"""
    
    # some words in references
    #TODO: fix "see also"
    
    inp_tag_text = inp_tag_text.replace("see also", " ")
    # long book name for Song of Solomon
    inp_tag_text = re.sub(r'((?<=[0-9])+[а-д])', '', inp_tag_text)
    inp_tag_text = re.sub(r'((?<=[0-9])+\s[а-д])', '', inp_tag_text)
    inp_tag_text = inp_tag_text.replace("Иисуса Навина", "Навина")
    inp_tag_text = inp_tag_text.replace("Песнь Песней", "Песн.")
    inp_tag_text = inp_tag_text.replace("Песни Песней", "Песн.")
    inp_tag_text = inp_tag_text.replace("Плач Иеремии", "Плач")
    inp_tag_text = inp_tag_text.replace("К римлянам", "Рим.")
    inp_tag_text = inp_tag_text.replace("к римлянам", "Рим.")
    inp_tag_text = inp_tag_text.replace("к ефесянам", "Ефесянам")
    inp_tag_text = inp_tag_text.replace("Псалмы", "Псалом")
    inp_tag_text = inp_tag_text.replace("псалмы", "Псалом")
    inp_tag_text = inp_tag_text.replace("Евангелие от", "")
    inp_tag_text = inp_tag_text.replace("от Марка", "Марка")
    inp_tag_text = inp_tag_text.replace("от Матфея", "Матфея")
    inp_tag_text = inp_tag_text.replace("от Луки", "Луки")
    inp_tag_text = inp_tag_text.replace("от Иоанна", "Иоанна")
    inp_tag_text = inp_tag_text.replace("Послание", "")
    inp_tag_text = inp_tag_text.replace("к евреям", "Евреям")
    inp_tag_text = inp_tag_text.replace("Стихи", "")
    inp_tag_text = inp_tag_text.replace("стих", "")
    inp_tag_text = inp_tag_text.replace("главы", "")
    inp_tag_text = inp_tag_text.replace("Главы", "")
    inp_tag_text = inp_tag_text.replace("главы", "")
    inp_tag_text = inp_tag_text.replace("гл.", "")
    inp_tag_text = inp_tag_text.replace(" и ", "; ")
    inp_tag_text = inp_tag_text.replace("начало", "")
    inp_tag_text = inp_tag_text.replace("–", "-")
    inp_tag_text = inp_tag_text.replace("'", "’")
    return inp_tag_text

#TODO: check this, dict replaced with { for avoiding a warning
book_index_to_MyBible = dict([\
#book_index_to_MyBible = {[\
('Быт',10),\
('Бытие',10),\
('Исх',20),\
('Исход',20),\
('Лев',30),\
('Левит',30),\
('Чис',40),\
('Числ',40),\
('Числа',40),\
('Втор',50),\
('Второзаконие',50),\
('Нав',60),\
('Навина',60),\
('Суд',70),\
('Судей',70),\
('Руфь',80),\
('Руф',80),\
('1Цар',90),\
('1Царств',90),\
('2Цар',100),\
('2Царств',100),\
('3Цар',110),\
('3Царств',110),\
('4Цар',120),\
('4Царств',120),\
('Иудф',180),\
('1Пар',130),\
('1Паралипоменон',130),\
('2Пар',140),\
('2Паралипоменон',140),\
('Ездр',150),\
('Езд',150),\
('Ездра',150),\
('Ездры',150),\
('Неем',160),\
('Неемии',160),\
('Неемия',160),\
('2Езд',165),\
('Тов',170),\
('Есф',190),\
('Есфирь',190),\
('Иов',220),\
('Иова',220),\
('Пс',230),\
('Псалом',230),\
('Псалтирь',230),\
('Прит',240),\
('Притч',240),\
('Притчи',240),\
('Еккл',250),\
('Песн',260),\
('Песней',260),\
('Прем',270),\
('Сир',280),\
('Ис',290),\
('Исаии',290),\
('Исаия',290),\
('Иер',300),\
('Иеремии',300),\
('Иеремия',300),\
('Плач',310),\
('Посл',315),\
('Вар',320),\
('Иез',330),\
('Иезекииля',330),\
('Иезекииль',330),\
('Дан',340),\
('Даниила',340),\
('Даниил',340),\
('Ос',350),\
('Осии',350),\
('Иоил',360),\
('Иоиля',360),\
('Ам',370),\
('Амоса',370),\
('Авд',380),\
('Ион',390),\
('Ионы',390),\
('Иона',390),\
('Мих',400),\
('Михея',400),\
('Михей',400),\
('Наум',410),\
('Авв',420),\
('Аввакума',420),\
('Соф',430),\
('Софонии',430),\
('Софония',430),\
('Агг',440),\
('Аггея',440),\
('Аггей',440),\
('Зах',450),\
('Захарии',450),\
('Захария',450),\
('Мал',460),\
('Малахии',460),\
('Малахия',460),\
('1Мак',462),\
('2Мак',464),\
('3Мак',466),\
('3Езд',468),\
('Мат',470),\
('Матфея',470),\
('Мф',470),\
('Мар',480),\
('Марка',480),\
('Мк',480),\
('Лук',490),\
('Луки',490),\
('Luke',490),\
('Лк',490),\
('Ин',500),\
('Иоанна',500),\
('Деян',510),\
('Деяния',510),\
('Иак',660),\
('Иакова',660),\
('1Пет',670),\
('1Петр',670),\
('1Петра',670),\
('2Пет',680),\
('2Петр',680),\
('2Петра',680),\
('1Ин',690),\
('1Иоанна',690),\
('2Ин',700),\
('2Иоанна',700),\
('3Ин',710),\
('3Иоанна',710),\
('Иуд',720),\
('Иуды',720),\
('Рим',520),\
('Римлянам',520),\
('1Кор',530),\
('1Коринфянам',530),\
('2Кор',540),\
('2Коринфянам',540),\
('Гал',550),\
('Галатам',550),\
('Еф',560),\
('Ефесянам',560),\
('Флп',570),\
('Филиппийцам',570),\
('Филиппийцам',570),\
('Фил',570),\
('Кол',580),\
('Колоссянам',580),\
('1Фес',590),\
('1Фессалоникийцам',590),\
('2Фес',600),\
('2Фессалоникийцам',600),\
('1Тим',610),\
('1Тимофею',610),\
('2Тим',620),\
('2Тимофею',620),\
('Тит',630),\
('Титу',630),\
('Флм',640),\
('Филимону',640),\
('Евр',650),\
('Евреям',650),\
('Откр',730),\
('Отк',730),\
('Откровение',730),\
('Лаод',780),\
('Мол',790),\
])
#]}
