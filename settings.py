import yaml
import pymysql.cursors
import requests
import json

with open('config/settings.yaml') as yaml_config:
	config_map = yaml.load(yaml_config)

# Token of your telegram bot that you created from @BotFather, write it on settings.yaml
TOKEN = config_map["token"]
API_URL = config_map["api_url"]

def read_remote_db():
    global dipartimenti
    global cds
    global materie

    dipartimenti = json.loads(requests.get("http://" + API_URL + "/dipartimenti").text)
    cds = json.loads(requests.get("http://" + API_URL + "/cds").text)
    materie = json.loads(requests.get("http://" + API_URL + "/materie").text)

def read_db_conf():
    global db_connection
    conf = open("config/dbconf.yaml", "r")
    doc = yaml.safe_load(conf)
    try:
        db_connection = pymysql.connect(
            host=doc["db_host"],
            user=doc["db_user"],
            passwd=doc["db_psw"],
            db=doc["db_name"],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except Exception as e:
        print("DB connection error")
        print(e)
    return
