import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.constants import END
import tkinter.scrolledtext as scrolledtext
import pyudev
import _thread
import pandas
import os
import subprocess
from dotenv import load_dotenv
import db
import dotenvpars as dp
import detodev as dv
import rfid
import datetime
import socket



class MainGui:
    def __init__(self, master):
        self.master = master
        pad=3
        self._geom='200x210+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.wm_attributes('-type', 'splash')
        tk.Label(self.master, text="Das Jufö Bankensystem").pack(anchor='center',pady=5)

        self.scrollbar = Scrollbar(self.master)
        self.scrollbar.pack( side = RIGHT, fill = Y )
        self.userlist = Listbox(self.master, yscrollcommand = self.scrollbar.set, width=60, height=15)

        for id,entry in db.Db().command("Select * From openpay.history;"):
            self.userlist.insert(END, str(entry))

        self.userlist.pack()
        self.scrollbar.config( command = self.userlist.yview )


    def update(self):
        self.userlist.delete(0,'end')
        for id,entry in db.Db().command("Select * From openpay.history;"):
            self.userlist.insert(END, str(entry))
            self.userlist.see(END)
        self.master.after(1000, self.update)

class Users:
    def __init__(self, master):
        self.master = master
        self.users = db.Db().command("Select * From users;")
        self._geom='200x210+0+0'
        master.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth()-3, master.winfo_screenheight()-3))
        master.wm_attributes('-type', 'splash')

        self.scrollbar = Scrollbar(self.master)
        self.scrollbar.pack( side = RIGHT, fill = Y )

        self.userlist = Listbox(self.master, yscrollcommand = self.scrollbar.set, width=60, height=15)
        self.userlist.insert(END, "TagID, Vorname, Nachname, Kontostand")
        for ID, tagid, name, nachname, kontostand, changes in self.users:
           self.userlist.insert(END, "{} {} {} {}".format(tagid, name, nachname, kontostand))

        self.userlist.pack()
        self.scrollbar.config( command = self.userlist.yview )

        tk.Button(self.master, text = 'Schließen', width = 25,command =  self.master.destroy).pack(anchor='center',side = BOTTOM)

class CardManage:
    def __init__(self, master,id):
        self.id = id
        self.betrag=""
        self.users = db.Db().command("Select * From users Order by name;")
        master.attributes('-fullscreen', True)
        self.master = master

        if db.Db().command("Select * From users Where tagid='{}';".format(id)) == []:
            #Tag not assigned
            tk.Label(self.master, text="Karte nicht in DB registriert. Karte mit Nutzer verknüpfen?").pack(anchor='center',pady=5)

            self.scrollbar = Scrollbar(self.master)
            self.scrollbar.pack( side = RIGHT, fill = Y )

            self.userlist = Listbox(self.master, yscrollcommand = self.scrollbar.set, width=60, height=13)
            self.userlist.insert(END, "TagID, Vorname, Nachname, Kontostand")
            for ID, tagid, name, nachname, kontostand, changes in self.users:
               self.userlist.insert(END, "{} {} {} {}".format(tagid, name, nachname, kontostand))

            self.userlist.pack()
            self.scrollbar.config( command = self.userlist.yview )

            tk.Button(self.master, text = 'Schließen', width = 10, command = self.master.destroy).pack(side = LEFT)
            tk.Button(self.master, text = 'Weiter', width = 10, command = self.select).pack(side = LEFT)

        else:
            self.userinfo = tk.Label(self.master, text = "Bitte Ausweis überprüfen: \n "+str(db.Db().command("Select * From users Where tagid='{}';".format(id))[0][2:6]).replace("'","").replace(",",""))
            self.userinfo.pack(anchor='center',pady=5)
            tk.Button(self.master, text = 'Einzahlen', width = 35, height=5, command=self.ein).pack(anchor='center',pady=5)
            tk.Button(self.master, text = 'Auszahlen', width = 35, height=5, command=self.aus).pack(anchor='center',pady=5)
            tk.Button(self.master, text = 'Schließen', width = 8, command = self.master.destroy).pack(anchor='center',pady=5)


    def select(self):
        if len(self.userlist.curselection()) == 0 or 0 in self.userlist.curselection():
            messagebox.showwarning("Auswahl", "Leider keine oder ungültige Auswahl!")

        userid_selection = self.users[self.userlist.curselection()[0]-1][0]
        db.Db().add_tag(self.id,userid_selection)
        self.master.destroy()

    def ein(self):
        self.betrag=""
        self.open_calc()

    def aus(self):
        self.betrag="-"
        self.open_calc()

    def press(self,number):
        self.betrag += str(number)
        self.btlabel['text']+=str(number)

    def back(self):
        if len(self.betrag) > 1 or len(self.betrag)==1 and self.betrag[0] != "-":
            self.betrag = self.betrag[:len(self.betrag)-1]
            self.btlabel['text']= self.betrag
    def go(self):
        user = db.Db().command("Select * From users Where tagid='{}';".format(self.id))[0]
        db.Db().new_betrag(self.id,float(self.betrag))
        db.Db().insert_entry("{} {} hat {} Taler übertragen bekommen ".format(user[2],user[3],self.betrag))

        MsgBox = tk.messagebox.showinfo('Zahlung hinterlegt','Betrag wurde verrechnet!',parent=self.master)
        if MsgBox == 'ok':
            self.app.destroy()
            self.master.destroy()

    def open_calc(self):

        self.app= tk.Toplevel(self.master)
        self.btlabel = tk.Label(self.app,text=self.betrag, font=("Courier", 24))
        self.btlabel.grid(row= 1,column=0, columnspan=3)

        tk.Button(self.app, text=' 1 ',command=lambda: self.press(1), height=2, width=9).grid(row=2, column=0)
        tk.Button(self.app, text=' 2 ',command=lambda: self.press(2), height=2, width=9).grid(row=2, column=1)
        tk.Button(self.app, text=' 3 ',command=lambda: self.press(3), height=2, width=9).grid(row=2, column=2)
        tk.Button(self.app, text=' 4 ',command=lambda: self.press(4), height=2, width=9).grid(row=3, column=0)
        tk.Button(self.app, text=' 5 ',command=lambda: self.press(5), height=2, width=9).grid(row=3, column=1)
        tk.Button(self.app, text=' 6 ',command=lambda: self.press(6), height=2, width=9).grid(row=3, column=2)
        tk.Button(self.app, text=' 7 ',command=lambda: self.press(7), height=2, width=9).grid(row=4, column=0)
        tk.Button(self.app, text=' 8 ',command=lambda: self.press(8), height=2, width=9).grid(row=4, column=1)
        tk.Button(self.app, text=' 9 ',command=lambda: self.press(9), height=2, width=9).grid(row=4, column=2)
        tk.Button(self.app, text=' 0 ',command=lambda: self.press(0), height=2, width=9).grid(row=5, column=1)
        tk.Button(self.app, text=' X ',command=self.back, height=2, width=9).grid(row=5, column=2)
        tk.Button(self.app, text=' , ',command=lambda: self.press("."), height=2, width=9).grid(row=5, column=0)

        tk.Button(self.app, text = 'Schließen', width = 8, command = self.app.destroy).grid(row=6, column=1, columnspan=1, padx=5, pady=5)
        tk.Button(self.app, text = 'Weiter', command=self.go, width = 8).grid(row=6, column=2, columnspan=1, padx=5, pady=5)

class SetAdminPass:
    def __init__(self, master):
        self.passwd = ""
        self.master = master
        self.frame = tk.Frame(self.master)

        self.pwlabel = tk.Label(self.frame,text="")
        self.pwlabel.grid(row= 1,column=0, columnspan=3)

        tk.Button(self.frame, text=' 1 ',command=lambda: self.press(1), height=1, width=7).grid(row=2, column=0)
        tk.Button(self.frame, text=' 2 ',command=lambda: self.press(2), height=1, width=7).grid(row=2, column=1)
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
        if len(self.passwd) == 4:
            dp.rewrite("ADMIN_PASS",str(self.passwd))
            MsgBox = tk.messagebox.showinfo('Admin Passwort','Das Adminpasswort wurde geändert! Änderungen werden nach einem Neustart wirksam.',parent=self.master)
            if MsgBox == 'ok':
                load_dotenv()
                self.master.destroy()







class Settings:
    def __init__(self, master):
        self.master = master
        self.switch_variable = tk.StringVar(value="static")
        pad=3
        self._geom='200x210+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.wm_attributes('-type', 'splash')
        self.frame = tk.Frame(self.master)

        tk.Label(self.frame, text="Die CSV Datei muss UTF_8 \n mit einem Komma als Begrenzung \n gespeichert werden!", height= 5).grid(row=0, column=0, columnspan=1, rowspan=2)



        tk.Button(self.frame, text = 'Datenabank sichern', width = 25, command=self.save_db).grid(row=2, column=0, columnspan=1)
        tk.Button(self.frame, text = 'Nutzerliste', width = 25,command=self.open_users).grid(row=3, column=0)
        tk.Button(self.frame, text = 'Passwort für Einstellungen ändern', width = 25, command=self.setpass).grid(row=4, column=0)
        tk.Button(self.frame, text = 'Datenbank leeren', width = 25, command = self.clear_db).grid(row=5, column=0)
        tk.Button(self.frame, text = 'Historie leeren', width = 25, command = self.clear_hs).grid(row=6, column=0)

        tk.Label(self.frame, text=self.get_ip()).grid(row=0, column=1,columnspan=2)
        tk.Button(self.frame, text = 'Leere CSV speichern', width = 25, command=self.save_csv).grid(row=1, column=1, columnspan=2)
        tk.Button(self.frame, text = 'Nutzer CSV einlesen', width = 25, command=self.load_csv).grid(row=2, column=1, columnspan=2)


        tk.Radiobutton(self.frame, text="Statische IP", variable=self.switch_variable,
                            indicatoron=False, value="static", width=12, command=lambda:_thread.start_new_thread(self.set_static,())).grid(row=3, column=1, columnspan=1)

        tk.Radiobutton(self.frame, text="DHCP", variable=self.switch_variable,
                                     indicatoron=False, value="dhcp", width=12, command=lambda:_thread.start_new_thread(self.set_dhcp,())).grid(row=3, column=2, columnspan=1)

        tk.Button(self.frame, text = 'System Verlinkung', width = 25, command=lambda:_thread.start_new_thread(self.link,())).grid(row=4, column=1, columnspan=2)
        tk.Button(self.frame, text = 'System Update', width = 25, command=lambda:_thread.start_new_thread(self.update,())).grid(row=5, column=1, columnspan=2)
        tk.Button(self.frame, text = 'Reboot', width = 25, command=lambda:_thread.start_new_thread(self.reboot,())).grid(row=6, column=1, columnspan=2)
        tk.Button(self.frame, text = 'Restart Program', width = 25, command=sys.exit).grid(row=7, column=1, columnspan=2)


        tk.Button(self.frame, text = 'Schließen', width = 10, command = self.master.destroy).grid(row=8, column=0, columnspan=2)
        self.frame.grid()

    def set_device(self,evt):
        # listeAusgewaehlt = self.listboxNamen.curselection()
        # itemAusgewaehlt = listeAusgewaehlt[0]
        # device = self.listboxNamen.get(itemAusgewaehlt)
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        dp.rewrite("DB_IP",str(value))
        MsgBox = tk.messagebox.showinfo('Systemlink','Das Quellgerät wurde geändert! Änderungen werden nach einem Neustart wirksam. Falls auf dem Ziel kein SQL Server läuft, wird auf die lokale Datenbank zugegriffen!',parent=self.master)
        if MsgBox == 'ok':
            self.top.destroy()



    def link(self):
        self.top = tk.Toplevel()
        self.top.wm_title("Datenbank Verlinkung")
        tk.Label(self.top, text="Bitte einen Moment warten!").grid(row=0, columnspan=2)
        self.listboxNamen = Listbox(self.top, selectmode='browse')
        self.listboxNamen.grid(row=1, column=0)
        self.listboxNamen.bind('<<ListboxSelect>>', self.set_device)
        self.listboxNamen.insert('end', '127.0.0.1')
        self.yScroll = Scrollbar(self.top, orient='vertical')
        self.yScroll.grid(row=1, column=1, sticky='ns')
        self.listboxNamen.config(yscrollcommand=self.yScroll.set)
        self.yScroll.config(command=self.listboxNamen.yview)

        tk.Button(self.top, text = 'Schließen', width = 10, command = self.top.destroy).grid(row=2, column=0, columnspan=2)

        devices = dv.get_active_devices()

        for device in devices:
            self.listboxNamen.insert('end', device)


    def set_dhcp(self):
        with open('/etc/dhcpcd.conf','w') as f:
            f.write(os.getenv("DHCP_CONFIG"))
        os.system("sudo ifdown eth0")
        os.system("sudo ifup eth0")
        os.system("sudo service networking restart")

    def set_static(self):
        with open('/etc/dhcpcd.conf','w') as f:
            f.write(os.getenv("NO_DHCP_CONFIG"))
        os.system("sudo ifdown eth0")
        os.system("sudo ifup eth0")
        os.system("sudo service networking restart")

    def get_ip(self):
        try:
            #only show ipv6 (split 2003)
            return subprocess.check_output("hostname -I", shell=True).decode('utf-8').replace("\n","").replace(" ","\n").split("2003",1)[0]
        except:
            return "Unable to get IP"

    def open_users(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Users(self.newWindow)

    def setpass(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = SetAdminPass(self.newWindow)

    def clear_db(self):
        MsgBox = tk.messagebox.askquestion ('Nutzerdatenbank leeren','Bist Du sicher, dass alle Nutzer gelöscht werden sollen?',icon = 'warning',parent=self.master)
        if MsgBox == 'yes':
           db.Db().del_all_users()

    def clear_hs(self):
        MsgBox = tk.messagebox.askquestion ('Verlauf leeren','Bist Du sicher, dass der Verlauf der Transaktionen gelöscht werden soll?',icon = 'warning',parent=self.master)
        if MsgBox == 'yes':
           db.Db().del_history()

    def load_csv(self):
        os.system("sudo fdisk -l")
        os.system("sudo pmount /dev/sda")

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

        for index, row in pandas.read_csv(csv_path, sep=',').iterrows():
                db.Db().insert_user([row["name"],row["nachname"]])

        try:
            os.system("sudo pumount --yes-I-really-want-lazy-unmount /dev/sda")
        except Exception as e:
            print(e)

    def save_csv(self):
        os.system("sudo fdisk -l")
        os.system("sudo pmount /dev/sda")

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

    def save_db(self):
        os.system("sudo fdisk -l")
        os.system("sudo pmount /dev/sda")

        root = tk.Tk()
        root.withdraw()
        root.overrideredirect(True)
        root.geometry('0x0+0+0')
        root.deiconify()
        root.lift()
        root.focus_force()
        db_path = filedialog.asksaveasfile(parent=root, mode='w',title="Datenbank sichern", initialdir = "/media/sda",
                    initialfile="userdata",defaultextension=".db",filetypes = (("db","*.db"),))
        root.destroy()
        if db_path is None:
            return

        try:
            os.system("sudo cp /home/pi/jufö/userdata.db {0}".format(db_path.name))
            os.system("sudo pumount --yes-I-really-want-lazy-unmount /dev/sda")

        except Exception as e:
            print(e)

    def update(self):
        self.top = tk.Toplevel()
        self.top.wm_title("Updating")

        self.status = tk.Text(self.top, width=50, height=8)
        self.status.grid(row=1,column=0)
        tk.Button(self.top, text = 'Schließen', width = 10, command = self.top.destroy).grid(row=2, column=0)

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
        tk.Button(self.frame, text=' 2 ',command=lambda: self.press(2), height=1, width=7).grid(row=2, column=1)
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
            #close all instances of Card
            self.newWindow = tk.Toplevel(self.master)
            self.app = CardManage(self.newWindow,id)

def setiptostatic():
    with open('/etc/dhcpcd.conf','w') as f:
        f.write(os.getenv("NO_DHCP_CONFIG"))
    os.system("sudo ifdown eth0")
    os.system("sudo ifup eth0")
    os.system("sudo service networking restart")


if __name__ == '__main__':
    try:
        os.system("sudo pumount --yes-I-really-want-lazy-unmount /dev/sda")
        os.system("sudo umount -l /media/*")
        os.system("sudo rm -r /media/*")
    except:
        pass

    load_dotenv()
    #set ip to static for link
    _thread.start_new_thread( setiptostatic,())



    root = tk.Tk()
    app = MainGui(root)

    root.after(1000, app.update())
    _thread.start_new_thread( CheckforUsb, (root, ) )

    _thread.start_new_thread( CheckforRfid, (root, ))

    root.mainloop()
