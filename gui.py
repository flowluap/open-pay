import tkinter as tk
from tkinter import filedialog, messagebox
import pyudev
import _thread
import pandas
import os
import db
import subprocess
from dotenv import load_dotenv
import db
import rfid



class MainGui:
    def __init__(self, master):
        self.master = master
        pad=3
        self._geom='200x210+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.wm_attributes('-type', 'splash')
        tk.Label(self.master, text="Das Jufö Bankensystem").pack(anchor='center',pady=5)
        #tk.Button(self.master, text = 'Einzahlen', width = 45,height=7).pack(anchor='center',pady=5)
        #tk.Button(self.master, text = 'Auszahlen', width = 45,height=7).pack(anchor='center',pady=5)
        tk.Button(self.master, text = 'Kill', width = 25,command =  self.master.destroy).pack(anchor='center')

class CardManage:
    def __init__(self, master,id):
        self.id = id
        self.master = master

        self._geom='200x210+0+0'
        master.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth()-3, master.winfo_screenheight()-3))
        master.wm_attributes('-type', 'splash')

        tk.Label(self.master, text=self.id).pack(anchor='center',pady=5)
        print()
        if db.Db().command("Select * From users Where tagid='{}';".format(id)).fetchall() == []:
            self.users = db.Db().command("Select * From users;").fetchall()
            print(self.users)
            tk.Label(self.master, text="Karte nicht in DB registriert. Karte mit Nutzer verknüpfen?").pack(anchor='center',pady=5)
        #else:
        tk.Button(self.master, text = 'Schließen', width = 10, command = self.master.destroy).pack()

class Settings:
    def __init__(self, master):
        self.master = master
        pad=3
        self._geom='200x210+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.wm_attributes('-type', 'splash')
        self.frame = tk.Frame(self.master)

        tk.Label(self.frame, text="Die CSV Datei muss UTF_8 \n mit einem Komma als Begrenzung \n gespeichert werden!", height= 5).grid(row=0, column=0, columnspan=1, rowspan=2)
        tk.Button(self.frame, text = 'Leere CSV speichern', width = 25, command=self.save_csv).grid(row=0, column=1, columnspan=1)
        tk.Button(self.frame, text = 'Nutzer CSV einlesen', width = 25, command=self.load_csv).grid(row=1, column=1, columnspan=1)
        tk.Button(self.frame, text = 'Datenbank leeren', width = 25, command = self.clear_db).grid(row=2, column=0)
        tk.Button(self.frame, text = 'Passwort für Einstellungen ändern', width = 25).grid(row=3, column=0)
        tk.Button(self.frame, text = 'Systemlink herstellen', width = 25).grid(row=2, column=1)
        tk.Button(self.frame, text = 'System Update', width = 25, command=lambda:_thread.start_new_thread(self.update,())).grid(row=3, column=1)
        tk.Button(self.frame, text = 'Reboot', width = 25, command=lambda:_thread.start_new_thread(self.reboot,())).grid(row=4, column=1)
        self.status = tk.Text(self.frame, width=50, height=5)
        self.status.grid(row=7,column=0,columnspan=2)
        tk.Button(self.frame, text = 'Schließen', width = 10, command = self.master.destroy).grid(row=8, column=0, columnspan=2)
        self.frame.grid()

        #self.master.update_idletasks()

    def clear_db(self):
        MsgBox = tk.messagebox.askquestion ('Nutzerdatenbank leeren','Bist Du sicher, dass alle Nutzer gelöscht werden sollen?',icon = 'warning',parent=self.master)
        if MsgBox == 'yes':
           db.Db().del_all_users()

    def load_csv(self):
        try:
            os.system("sudo pmount /dev/sda")
        except:
            pass

        root = tk.Tk()
        root.withdraw()
        root.overrideredirect(True)
        root.geometry('0x0+0+0')
        root.deiconify()
        root.lift()
        root.focus_force()
        csv_path = filedialog.askopenfilename(parent=root, initialdir = "/media/sda",title = "CSV auswählen",filetypes = (("csv Dateien","*.csv"),("all files","*.*")))
        root.destroy()
        if csv_path is None or len(csv_path) < 1:
            return
        #print(pandas.read_csv(csv_path,sep=',', encode="utf8"))

        for index, row in pandas.read_csv(csv_path, sep=',').iterrows():
                print(row["name"],row["nachname"], row["Geburtsdatum (alternativ)"])
                db.Db().insert_user([row["name"],row["nachname"], row["Geburtsdatum (alternativ)"]])




        try:
            os.system("sudo cp /home/pi/jufö/empty.csv {0}".format(csv_path.name))
            print("sudo cp /home/pi/jufö/empty.csv {0}".format(csv_path.name))
            os.system("sudo pumount --yes-I-really-want-lazy-unmount /dev/sda")
        except Exception as e:
            print(e)

    def save_csv(self):
        try:
            os.system("sudo pmount /dev/sda")
        except:
            pass

        root = tk.Tk()
        root.withdraw()
        root.overrideredirect(True)
        root.geometry('0x0+0+0')
        root.deiconify()
        root.lift()
        root.focus_force()
        csv_path = filedialog.asksaveasfile(parent=root, mode='w',title="Leere CSV speichern", initialdir = "/media/sda",
                    initialfile="leer",defaultextension=".csv",filetypes = (("csv","*.csv"),))
        root.destroy()
        if csv_path is None:
            return

        try:
            os.system("sudo cp /home/pi/jufö/empty.csv {0}".format(csv_path.name))
            os.system("sudo pumount --yes-I-really-want-lazy-unmount /dev/sda")

        except Exception as e:
            print(e)
            #pass


    def update(self):
        with subprocess.Popen(["sudo apt-get update -y && sudo apt-get upgrade -y"], shell=True, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True) as p:
            for line in p.stdout:
                self.status.delete("1.0", "end")
                self.status.insert(tk.END, line)


    def reboot(self):
        os.system('sudo reboot')


class CheckAdminPass:
    def __init__(self, master):
        self.passwd = ""
        self.master = master
        self.frame = tk.Frame(self.master)

        self.pwlabel = tk.Label(self.frame,text="")
        self.pwlabel.grid(row= 1,column=0, columnspan=3)

        tk.Button(self.frame, text=' 1 ',command=lambda: self.press(1), height=1, width=7).grid(row=2, column=0)
        tk.Button(self.frame, text=' 2 ',command=lambda: self.press(1), height=1, width=7).grid(row=2, column=1)
        tk.Button(self.frame, text=' 3 ',command=lambda: self.press(3), height=1, width=7).grid(row=2, column=2)
        tk.Button(self.frame, text=' 4 ',command=lambda: self.press(4), height=1, width=7).grid(row=3, column=0)
        tk.Button(self.frame, text=' 5 ',command=lambda: self.press(5), height=1, width=7).grid(row=3, column=1)
        tk.Button(self.frame, text=' 6 ',command=lambda: self.press(6), height=1, width=7).grid(row=3, column=2)
        tk.Button(self.frame, text=' 7 ',command=lambda: self.press(7), height=1, width=7).grid(row=4, column=0)
        tk.Button(self.frame, text=' 8 ',command=lambda: self.press(8), height=1, width=7).grid(row=4, column=1)
        tk.Button(self.frame, text=' 9 ',command=lambda: self.press(9), height=1, width=7).grid(row=4, column=2)
        tk.Button(self.frame, text=' 0 ',command=lambda: self.press(0), height=1, width=7).grid(row=5, column=1)
        self.frame.grid()

    def press(self,number):
        self.passwd += str(number)
        self.pwlabel['text']+="*"
        if len(self.passwd) == 4 and self.passwd==os.getenv("ADMIN_PASS"):
            print("Password okay")
            self.newWindow = tk.Toplevel(self.master)
            self.app = Settings(self.newWindow)
            self.master.withdraw()

        if len(self.passwd) == 4:
            self.passwd = ""
            self.pwlabel['text']=""

class CheckforUsb:
    def __init__(self, master):
        self.master = master
        self.lastdevice=""
        context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by(subsystem='usb')
        for device in iter(monitor.poll, None):
            if device.action == 'add' and self.lastdevice not in str(device) or device.action == 'add' and self.lastdevice=="":
                print("[+] USB-Stick wurde erkannt")
                self.lastdevice = str(device)[:61]
                self.newWindow = tk.Toplevel(self.master)
                self.app = CheckAdminPass(self.newWindow)

            elif device.action == 'remove':
                print("[+] USB-Stick wurde entfernt")
                os.system("sudo pumount --yes-I-really-want-lazy-unmount /dev/sda")
                os.system("sudo umount -l /media/*")
                os.system("sudo rm -r /media/*")

class CheckforRfid:
    def __init__(self, master):
        self.master = master
        id = rfid.read()
        if id != None:
            _thread.start_new_thread( CheckforRfid, (root, ))
            print(id)
            #close all instances of Card
            self.newWindow = tk.Toplevel(self.master)
            self.app = CardManage(self.newWindow,id)




if __name__ == '__main__':
    os.system("sudo pumount --yes-I-really-want-lazy-unmount /dev/sda")
    os.system("sudo umount -l /media/*")
    os.system("sudo rm -r /media/*")

    load_dotenv()

    root = tk.Tk()
    app = MainGui(root)
    _thread.start_new_thread( CheckforUsb, (root, ) )

    _thread.start_new_thread( CheckforRfid, (root, ))

    root.mainloop()
