import yaml
import requests
import json
import sqlite3

with open('config/settings.yaml') as yaml_config:
	config_map = yaml.safe_load(yaml_config)

# Token of your telegram bot that you created from @BotFather, write it on settings.yaml
TOKEN = config_map["token"]
API_URL = config_map["api_url"]
CHAT_ID_TEST = config_map["chat_id_test"]

def read_remote_db():
    global dipartimenti
    global cds
    global materie

    try:
        dipartimenti = json.loads('[{"id": "D251", "name": "DMI", "annoAccademico": 2020}]')
        cds = json.loads(requests.get("http://" + API_URL + "/cdl?anno=2020&token=").text)
        materie = json.loads(requests.get("http://" + API_URL + "/materie?anno=2020&token=").text)
    except requests.exceptions.ConnectionError:
        return False

def read_remote_avvisi():
    avvisi = ""
    try:
        avvisi = json.loads(requests.get("http://" + API_URL + "/avvisi?anno=2020&token=").text)
    except requests.exceptions.ConnectionError:
        avvisi = False
    return avvisi

def read_db_conf():
    global db_connection
    try:
        db_connection = sqlite3.connect("data/studium.db", check_same_thread=False)
        db_connection.row_factory = sqlite3.Row
    except Exception as e:
        print("DB connection error")
        print(e)
    return

def query(sql):
    try:
        cursor = db_connection.cursor()
        cursor.execute(sql)
        if not(sql.startswith("SELECT")):
            db_connection.commit()
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(e)
        return False
