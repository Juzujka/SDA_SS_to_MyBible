# SDA_SS_to_MyBible

This project produces MyBible modules containing SDA Church Sabbath School lessons.
Each lesson contains daily devotionals.

## Getting started

If not installed, install Python 3 (version 3.8 or newer), pip, and venv

```
sudo apt install python3 python3-pip python3-venv
```

Clone the repository

```
git clone https://github.com/Juzujka/SDA_SS_to_MyBible.git
```

or download the ZIP archive and extract it into a local directory.

Create a virtual environment and install dependencies:

```
python3 -m venv .venv
source .venv/bin/activate
pip install beautifulsoup4 regex
```

Or install the required dependencies system-wide:

```
sudo apt install python3-bs4 python3-regex
```


Run the script with appropriate arguments, for example:


```
./SDA_SS_to_MyBible_devotions.py --year 2020 --lang ru --type ad --append
```

Arguments:

| Argument   | Description                                              |
|------------|----------------------------------------------------------|
| `--year`   | Year of the Sabbath School lessons                       |
| `--lang`   | Language code: `en`, `ru`, `es`, `uk`                    |
| `--type`   | `ad` for adult lessons, `ay` for youth lessons           |
| `--append` | If the database exists, add the new quarter to it        |

The script produces a module database file `SS-<lang>-<ad|ay>'<year>.devotions.SQLite3` (where `<year>` is the last two digits of the year, e.g. `26` for 2026) and updates `SDA-SS-<lang>-<ad|ay>.devotions.registry.json`.

The recommended way is to publish the file through an extra module registry, as described in the manual [MyBible for Android – extra module registries](https://mybible.zone/en/android/extra-registries/). On older Android versions, you can place module files in the MyBible application directory; newer versions do not allow this.
You can use [registry file from this project](https://raw.githubusercontent.com/Juzujka/SDA_SS_to_MyBible/master/SDA-SS-en-ad.devotions.registry.json) and replace its file links with the URLs where your files are published.

### About SS_to_MyBible

SDA Sabbath School materials are daily Bible study texts.
MyBible is an Android application for reading the Bible, with many features and modules. 

SS\_to\_MyBible gathers data from the adventech.io service, which provides SDA Sabbath School materials, and the script creates MyBible modules with clickable links to Bible texts. 

Because MyBible devotionals start on January 1, the lessons always start from the beginning of the year.
SDA\_SS\_to\_MyBible pulls lessons quarter by quarter from the beginning of the year to the last available quarter. 

Days from the previous year that belong to the current lesson are added to January 1 of the current year. 

The introduction is added to the first day of each quarter.

Data is pulled from adventech.io: https://github.com/Adventech/adventech.io

### Languages supported by the script

- English (`en`)
- Spanish (`es`)
- Russian (`ru`)
- Ukrainian (`uk`)

The script supports all four languages. However, not every Bible reference in new material may be recognized: the material is written by people, and editors often follow their own conventions for Bible book names and reference formatting. If a new reference format appears, update the corresponding `lang_XX.py` file to handle it.

### Available prebuilt modules

Modules are generated on request. If no request is received, no module is produced. As of Q4 2026, the repository contains generated modules for English, Spanish, and Russian. Modules for the other supported languages can be added on request.

## How to add modules from this repository to your MyBible application

Open your MyBible application.

Tap the three-dot menu in the upper-right corner → tap "Modules" → on the Modules screen, tap the three-dot menu in the upper-right corner → tap "Extra module registries" → tap "+" in the upper-right corner.

Fill in the URL field with the registry file URL for your language:

Russian - `https://raw.githubusercontent.com/Juzujka/SDA_SS_to_MyBible/master/SDA-SS-ru-ad.devotions.registry.json`  
English - `https://raw.githubusercontent.com/Juzujka/SDA_SS_to_MyBible/master/SDA-SS-en-ad.devotions.registry.json`  
Spanish - `https://raw.githubusercontent.com/Juzujka/SDA_SS_to_MyBible/master/SDA-SS-es-ad.devotions.registry.json`  

If you want the module in Russian and GitHub is inaccessible, there is an alternative source:

Russian - `https://gitverse.ru/api/repos/Juzujka/SDA_SS_to_MyBible/raw/branch/master/SDA-SS-ru-ad-gitverse.devotions.registry.json`

Select the module for the desired year and download it.

You can now find Sabbath School modules in the list of devotions.

Remember to update the module to get the material for the new quarter. Note that updates may sometimes arrive later.

If you need a Sabbath School module in another language, ask the author at <juzujka@gmail.com> or make it for yourself as described in the [Getting started](#getting-started) section.

## License

### Source code
The source code in this repository (scripts, parsers, and module generators) is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for the full text.

### Lesson content
The Sabbath School lesson content is **not** covered by the MIT License. It is © General Conference of Seventh-day Adventists. This project is not affiliated with or endorsed by the General Conference.

The generated modules are provided **for personal study only**. They are not intended for redistribution, sale, or any commercial use. If you are a copyright holder and have concerns, please contact the author.
