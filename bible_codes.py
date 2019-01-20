#! /usr/bin/env python3

book_index_to_MyBible = {}

book_index_to_MyBible['ru'] = dict([\
('Быт',10),\
('Исх',20),\
('Лев',30),\
('Чис',40),\
('Втор',50),\
('Нав',60),\
('Суд',70),\
('Руфь',80),\
('1Цар',90),\
('2Цар',100),\
('3Цар',110),\
('4Цар',120),\
('Иудф',180),\
('1Пар',130),\
('2Пар',140),\
('Ездр',150),\
('Неем',160),\
('2Езд',165),\
('Тов',170),\
('Есф',190),\
('Иов',220),\
('Пс',230),\
('Прит',240),\
('Притч',240),\
('Еккл',250),\
('Песн',260),\
('Прем',270),\
('Сир',280),\
('Ис',290),\
('Иер',300),\
('Плач',310),\
('Посл',315),\
('Вар',320),\
('Иез',330),\
('Дан',340),\
('Ос',350),\
('Иоил',360),\
('Ам',370),\
('Авд',380),\
('Ион',390),\
('Мих',400),\
('Наум',410),\
('Авв',420),\
('Соф',430),\
('Агг',440),\
('Зах',450),\
('Мал',460),\
('1Мак',462),\
('2Мак',464),\
('3Мак',466),\
('3Езд',468),\
('Мат',470),\
('Мф',470),\
('Мар',480),\
('Мк',480),\
('Лук',490),\
('Лк',490),\
('Ин',500),\
('Деян',510),\
('Иак',660),\
('1Пет',670),\
('1Петр',670),\
('2Пет',680),\
('2Петр',680),\
('1Ин',690),\
('2Ин',700),\
('3Ин',710),\
('Иуд',720),\
('Рим',520),\
('1Кор',530),\
('2Кор',540),\
('Гал',550),\
('Еф',560),\
('Флп',570),\
('Кол',580),\
('1Фес',590),\
('2Фес',600),\
('1Тим',610),\
('2Тим',620),\
('Тит',630),\
('Флм',640),\
('Евр',650),\
('Откр',730),\
('Отк',730),\
('Лаод',780),\
('Мол',790)\
])

book_index_to_MyBible['uk'] = dict([\
('Бут',10),\
('Вих',20),\
('Лев',30),\
('Левит',30),\
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
('Неєм',160),\
('Ест',190),\
('Йов',220),\
('Псал',230),\
('Прит',240),\
('Екк',250),\
('Екл',250),\
('П.Пісн',260),\
('Ісаї',290),\
('Єрем',300),\
('Пл.Єр',310),\
('Єзек',330),\
('Дан',340),\
('Осії',350),\
('Йоїла',360),\
('Йоіла',360),\
('Амоса',370),\
('Овд',380),\
('Йони',390),\
('Міх',400),\
('Наума',410),\
('Авак',420),\
('Соф',430),\
('Огія',440),\
('Зах',450),\
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
('Об’явлення',730)\
])

ru_to_MyBible = dict([\
('Быт',10),\
('Исх',20),\
('Лев',30),\
('Чис',40),\
('Втор',50),\
('Нав',60),\
('Суд',70),\
('Руфь',80),\
('1Цар',90),\
('2Цар',100),\
('3Цар',110),\
('4Цар',120),\
('Иудф',180),\
('1Пар',130),\
('2Пар',140),\
('Ездр',150),\
('Неем',160),\
('2Езд',165),\
('Тов',170),\
('Есф',190),\
('Иов',220),\
('Пс',230),\
('Прит',240),\
('Притч',240),\
('Еккл',250),\
('Песн',260),\
('Прем',270),\
('Сир',280),\
('Ис',290),\
('Иер',300),\
('Плач',310),\
('Посл',315),\
('Вар',320),\
('Иез',330),\
('Дан',340),\
('Ос',350),\
('Иоил',360),\
('Ам',370),\
('Авд',380),\
('Ион',390),\
('Мих',400),\
('Наум',410),\
('Авв',420),\
('Соф',430),\
('Агг',440),\
('Зах',450),\
('Мал',460),\
('1Мак',462),\
('2Мак',464),\
('3Мак',466),\
('3Езд',468),\
('Мат',470),\
('Мф',470),\
('Мар',480),\
('Мк',480),\
('Лук',490),\
('Лк',490),\
('Ин',500),\
('Деян',510),\
('Иак',660),\
('1Пет',670),\
('1Петр',670),\
('2Пет',680),\
('2Петр',680),\
('1Ин',690),\
('2Ин',700),\
('3Ин',710),\
('Иуд',720),\
('Рим',520),\
('1Кор',530),\
('2Кор',540),\
('Гал',550),\
('Еф',560),\
('Флп',570),\
('Кол',580),\
('1Фес',590),\
('2Фес',600),\
('1Тим',610),\
('2Тим',620),\
('Тит',630),\
('Флм',640),\
('Евр',650),\
('Откр',730),\
('Отк',730),\
('Откровение',730),\
('Лаод',780),\
('Мол',790)\
])
