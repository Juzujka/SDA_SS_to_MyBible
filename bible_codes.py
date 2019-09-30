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

book_index_to_MyBible = {}

book_index_to_MyBible['ru'] = dict([\
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
('Пс',230),\
('Псалом',230),\
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
('Лк',490),\
('Ин',500),\
('Иоанна',500),\
('Деян',510),\
('Деяния',510),\
('Иак',660),\
('Иакова',660),\
('1Пет',670),\
('1Петр',670),\
('2Пет',680),\
('2Петр',680),\
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

book_index_to_MyBible['uk'] = dict([\
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

book_index_to_MyBible['es'] = dict([\
('Génesis',10),\
('Gén',10),\
('Éxodo',20),\
('Éxo',20),\
('Levítico',20),\
('Lev',20),\
('Núm',40),\
('Números',40),\
('Deuteronomio',50),\
('Deut',50),\
('Josué',60),\
('Jos',60),\
('Jueces',70),\
('Juec',70),\
('Rut',80),\
('1Samuel',90),\
('1Sam',90),\
('2Samuel',100),\
('2Sam',100),\
('1Reyes',110),\
('1Rey',110),\
('2Reyes',110),\
('2Rey',110),\
('1Crónicas',130),\
('1Crón',130),\
('2Crónicas',140),\
('2Crón',130),\
('Esdras',150),\
('Esd',150),\
('Nehemías',160),\
('Neh',160),\
('Ester',190),\
('Est',190),\
('Job',220),\
('Salmos',230),\
('Salmo',230),\
('Sal',230),\
('Sals',230),\
('Proverbios',240),\
('Prov',240),\
('Eclesiastés',250),\
('Ecl',250),\
('Cantares',260),\
('Cant',260),\
('Isaías',290),\
('Isa',290),\
('Jeremías',300),\
('Jer',300),\
('Lam',310),\
('Lamentaciones',310),\
('La',310),\
('Ezequiel',330),\
('Eze',330),\
('Dan',340),\
('Daniel',340),\
('Oseas',350),\
('Os',350),\
('Joel',360),\
('Am',370),\
('Amós',370),\
('Amos',370),\
('Abdías',380),\
('Jonás',390),\
('Miqueas',400),\
('Miq',400),\
('Nah',410),\
('Nahum',410),\
('Hab',420),\
('Habacuc',420),\
('Sofonías',430),\
('Hag',440),\
('Hageo',440),\
('Zac',450),\
('Zacarías',450),\
('Mal',460),\
('Malaquías',460),\
('Mat',470),\
('Mateo',470),\
('Mar',480),\
('Marcos',480),\
('Luc',490),\
('Lucas',490),\
('Juan',500),\
('Hechos',510),\
('Hech',510),\
('Santiago',660),\
('Sant',660),\
('1Pedro',670),\
('1Ped',670),\
('2Pedro',680),\
('2Ped',680),\
('1Juan',690),\
('2Juan',700),\
('3Juan',710),\
('Rom',520),\
('Romanos',520),\
('1Cor',530),\
('1Corintios',530),\
('2Cor',540),\
('2Corintios',540),\
('Gál',550),\
('Gálatas',550),\
('Ef',560),\
('Efe',560),\
('Efesios',560),\
('Filipenses',570),\
('Fil',570),\
('Col',580),\
('Colosenses',580),\
('1Tes',590),\
('1Tesalonicenses',590),\
('2Tes',600),\
('2Tesalonicenses',600),\
('1Tim',610),\
('1Timoteo',610),\
('2Tim',620),\
('2Timoteo',620),\
('Tito',630),\
('Tit',630),\
('Ti',630),\
('Filemón',640),\
('Heb',650),\
('Hebreos',650),\
('Judas',720),\
('Jud',720),\
('Apoc',730),\
('Apocalipsis',730),\
])
