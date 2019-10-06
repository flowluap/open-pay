import os, sys, sqlite3

def create_db():
    connection = sqlite3.connect("/home/pi/jufö/userdata.db")
    cursor = connection.cursor()
    # Tabelle erzeugen
    sql = "CREATE TABLE users("\
        "name VARCHAR(30), nachname VARCHAR(30), kontostand FLOAT, \
         maxTempUser FLOAT) "
    cursor.execute(sql)
    connection.commit()
    connection.close()



if __name__=="__main__":
    if not os.path.exists("userdata.db"):
        create_db()
