import os, sys, sqlite3
import datetime
import mysql.connector as database
import dotenvpars as dp
import time

class Db():
    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv()
        try:
            self.mydb = database.connect(
              host=os.getenv("DB_IP"),
              port=3306,
              user="root",
              passwd="",
              autocommit=True
            )
            self.cursor = self.mydb.cursor(buffered=True)
            self.create_db()
        except Exception as e:
            print(e)
            #dp.rewrite("DB_IP",'127.0.0.1')
            time.sleep(1)
            self.mydb = database.connect(
              host='127.0.0.1',
              port=3306,
              user="root",
              passwd="",
              autocommit=True
            )
            self.cursor = self.mydb.cursor(buffered=True)
            self.create_db()



    def create_db(self):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS openpay")

        self.cursor.execute("USE openpay")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                  ID INTEGER PRIMARY KEY AUTO_INCREMENT,
                  tagid VARCHAR(65),
                  name VARCHAR(30),
                  nachname VARCHAR(30),
                  kontostand FLOAT,
                  changes VARCHAR(45)
                )""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS history(
                  ID INTEGER PRIMARY KEY AUTO_INCREMENT,
                  entry VARCHAR(120)
                );""")

    def command(self,sql):
        #potential sql injection
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        #self.cursor.close()

        return result

    def add_tag(self,id,userid_selection):

        self.cursor.execute("UPDATE openpay.users SET tagid = %s, changes = %s WHERE ID = %s;", (id,datetime.datetime.now(),int(userid_selection),))
        self.cursor.close()

    def new_betrag(self,id,betrag):
        alter_betrag = self.command("Select kontostand From users Where tagid='{}';".format(id))[0][0]
        neuer_betrag = alter_betrag + betrag
        self.cursor.execute("UPDATE users SET kontostand = %s, changes = %s WHERE tagid = %s;", (neuer_betrag,datetime.datetime.now(),id),)
        self.cursor.close()

    def del_all_users(self):
        sql = "Delete From users"
        self.cursor.execute(sql)
        self.cursor.close()

    def del_history(self):
        sql = "Delete From history"
        self.cursor.execute(sql)
        self.cursor.close()

    def insert_user(self,data):
        name, lastname = data
        sql = "Insert INTO users (name, nachname, kontostand, changes) Values ('{}','{}','{}','{}');".format(name, lastname, os.getenv("INITIAL_ACCOUNT_PLUS"),datetime.datetime.now())
        self.cursor.execute(sql)
        self.cursor.close()

    def insert_entry(self,entry):
        sql = "Insert INTO history (entry) Values ('{}');".format(entry)
        self.cursor.execute(sql)
        self.cursor.close()

if __name__ == "__main__":
    print(Db().command("SELECT * FROM openpay.history"))
