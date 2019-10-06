import os, sys, sqlite3
import datetime
from dotenv import load_dotenv

load_dotenv()

connection = sqlite3.connect("/home/pi/jufö/userdata.db")
cursor = connection.cursor()

class Db:
    def __init__(self):
        if not os.path.exists("userdata.db"):
            self.create_db()

        self.connection = sqlite3.connect("/home/pi/jufö/userdata.db")
        self.cursor = connection.cursor()

    def create_db(self):

        # Tabelle erzeugen
        sql = "CREATE TABLE users("\
            "tagid VARCHAR(65), name VARCHAR(30), nachname VARCHAR(30), birth VARCHAR(30), kontostand FLOAT, \
             change VARCHAR(45)) "
        self.cursor.execute(sql)
        self.connection.commit()
        self.connection.close()

    def del_all_users(self):
        os.system("sudo rm userdata.db")

        self.create_db()

    def insert_kid(self,data):

        name, lastname, birth = data

        sql = "Insert INTO users (name, nachname, geburtsdatum, kontostand, change) \
                Values (%s,%s,%s,%s,%s);",(name, lastname, birth, os.getenv("INITIAL_ACCOUNT_PLUS"),datetime.datetime.now(),)

        self.cursor.execute(sql)
        self.connection.commit()
        self.connection.close()
