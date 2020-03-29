# Useful links
## API:
https://adventech-sabbath-school.api-docs.io/v1/quarterlies/list-quarters

##Requests examples
Quarters list request
https://sabbath-school.adventech.io/api/v1/en/quarterlies/index.json

Lesson request
https://sabbath-school.adventech.io/api/v1/ru/quarterlies/2020-01/lessons/01/days/01/read/index.json

#How to run
cd ~/My_Designs/MyBible_SS/MyBible_SS_Python

./SDA_SS_to_MyBible_devotions.py --year 2020 --lang ru
or to append
./SDA_SS_to_MyBible_devotions.py --year 2020 --lang ru --type ay --append

to check resulting database
sqlitebrowser ./SDA_SS_2018_2_ru.devotions.sqlite3


Run test for debug

./SDA_SS_to_MyBible_devotions.py --year 2019 --lang ru --test_print_day --test_n_quart 2 --test_n_less 11 --test_n_day 1
