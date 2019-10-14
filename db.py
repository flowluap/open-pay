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
        os.system("sudo chmod 777 /home/pi/jufö/userdata.db")
        os.system("sudo chown pi /home/pi/jufö/userdata.db")
        sql = "CREATE TABLE IF NOT EXISTS users("\
            "ID INTEGER PRIMARY KEY AUTOINCREMENT, tagid VARCHAR(65), name VARCHAR(30), nachname VARCHAR(30), kontostand FLOAT, \
             change VARCHAR(45)) "
        self.cursor.execute(sql)
        sql = "CREATE TABLE IF NOT EXISTS history("\
            "ID INTEGER PRIMARY KEY AUTOINCREMENT, entry VARCHAR(120));"
        self.cursor.execute(sql)
        self.connection.commit()

    def command(self, sql):
        return self.cursor.execute(sql)
        self.connection.commit()

    def add_tag(self,id,userid_selection):
        self.cursor.execute("UPDATE users SET tagid = ?, change = ? WHERE ID = ?;", (id,datetime.datetime.now(),int(userid_selection),))
        self.connection.commit()

    def new_betrag(self,id,betrag):
        alter_betrag = self.command("Select kontostand From users Where tagid='{}';".format(id)).fetchall()[0][0]
        neuer_betrag = alter_betrag + betrag
        self.cursor.execute("UPDATE users SET kontostand = ?, change = ? WHERE tagid = ?;", (neuer_betrag,datetime.datetime.now(),id),)
        self.connection.commit()


    def del_all_users(self):
        sql = "Delete From users"
        self.cursor.execute(sql)
        self.connection.commit()

    def del_history(self):
        sql = "Delete From history"
        self.cursor.execute(sql)
        self.connection.commit()


    def insert_user(self,data):
        name, lastname = data
        sql = "Insert INTO users (name, nachname, kontostand, change) Values ('{}','{}','{}','{}');".format(name, lastname, os.getenv("INITIAL_ACCOUNT_PLUS"),datetime.datetime.now())
        self.cursor.execute(sql)
        self.connection.commit()

    def insert_entry(self,entry):
        sql = "Insert INTO history (entry) Values ('{}');".format(entry)
        self.cursor.execute(sql)
        self.connection.commit()
