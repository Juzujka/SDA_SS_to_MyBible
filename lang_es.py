#! /usr/bin/env python3
# encoding: utf-8

""" Internationalization for Spanish
 
 This module considers dictionary of
 pairs of variants of books of Bible abbreviations
 with its number in MyBible format, function for preprocessing references from text materials to the common format,
 and some text for internationalization.
 
"""

db_info_description_title = "Lecciones de la Escuela Sabática de la Iglesia Adventista del Séptimo Día"
db_info_description_version_adult = "para adultos"
db_info_description_version_youth = ""
db_info_description_list_of_quarterly_themes = "Lista de temas trimestrales"
db_info_description_from_author = """Para enviar comentarios y sugerencias sobre el módulo, use el servicio en <a href="https://github.com/Juzujka/SDA_SS_to_MyBible/issues"> https://github.com/Juzujka/SDA_SS_to_MyBible/issues </a>. Envíe agradecimientos, bendiciones, ofertas de ayuda y cooperación a juzujka@gmail.com."""
db_info_description_origin_text = """created by Egor Ibragimov, juzujka@gmail.com\nthe text is taken from sabbath-school.adventech.io"""
db_info_description_lesson = "la lección"
db_info_description_day = "el dia"


def ref_tag_preprocess(inp_tag_text):
    """adopting references in lessons in Spanish"""

    inp_tag_text = inp_tag_text.replace("–", "-")
    inp_tag_text = inp_tag_text.replace("'", "’")
    inp_tag_text = inp_tag_text.replace(" y ", ",")
    inp_tag_text = inp_tag_text.replace(" al ", "-")
    return inp_tag_text

book_index_to_MyBible = dict([\
('Génesis',10),\
('Genesis',10),\
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
('Isaias',290),\
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
('Nahúm',410),\
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
('1Tesalonisenses',590),\
('2Tes',600),\
('2Tesalonicenses',600),\
('2Tesalonisenses',600),\
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