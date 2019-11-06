# Telegram-Studium-DMI-Bot

---

### Setting up a local istance
If you want to test the bot by creating your personal istance, follow this steps:
* **Clone this repository** or download it as zip.
* **Send a message to your bot** on Telegram, even '/start' will do. If you don't, you could get an error
* Copy the file data/DMI_DB.db.dist into data/DMI_DB.db to enable the database sqlite
* Copy the file config/settings.yaml.dist into config/settings.yaml (If you don't have a token, message Telegram's [@BotFather](http://telegram.me/Botfather) to create a bot and get a token for it)
* Now you can launch "main.py" with your Python3 interpreter

### System requirements

- Python 3
- python-pip3
- sqlite3

#### To install with *pip3*

- pip3 install -r requirements.txt


### Database setup

- $ sqlite3 studium.db < Studium_DB.sql 


### License
This open-source software is published under the GNU General Public License (GNU GPL) version 3. Please refer to the "LICENSE" file of this project for the full text.
