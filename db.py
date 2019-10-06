import os, sys, sqlite3
import datetime
from dotenv import load_dotenv

load_dotenv()

connection = sqlite3.connect("/home/pi/jufö/userdata.db")
cursor = connection.cursor()

class Db:
    def __init__(self):
        self.connection = sqlite3.connect("/home/pi/jufö/userdata.db")
        self.cursor = self.connection.cursor()
        self.create_db()

    def create_db(self):
        os.system("chmod 664 /home/pi/jufö/userdata.db")
        sql = "CREATE TABLE IF NOT EXISTS users("\
            "tagid VARCHAR(65), name VARCHAR(30), nachname VARCHAR(30), birth VARCHAR(30), kontostand FLOAT, \
             change VARCHAR(45)) "
        self.cursor.execute(sql)
        self.connection.commit()

    def command(self, sql):
        return self.cursor.execute(sql)
        self.connection.commit()
        self.connection.close()

    def del_all_users(self):
        sql = "Delete From users"
        self.cursor.execute(sql)
        self.connection.commit()
        self.connection.close()

    def insert_user(self,data):
        name, lastname, birth = data
        sql = "Insert INTO users (name, nachname, birth, kontostand, change) Values ('{}','{}','{}','{}','{}');".format(name, lastname, birth, os.getenv("INITIAL_ACCOUNT_PLUS"),datetime.datetime.now())
        self.cursor.execute(sql)
        self.connection.commit()
        self.connection.close()
