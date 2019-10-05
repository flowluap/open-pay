import tkinter as tk
import pyudev
import _thread
import os

class MainGui:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)

        tk.Button(self.frame, text = 'Einzahlen', width = 25).grid()
        tk.Button(self.frame, text = 'Auszahlen', width = 25).grid()
        tk.Button(self.frame, text = 'Kill', width = 25,command =  self.master.destroy).grid()
        self.frame.grid()


class Settings:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)

        tk.Button(self.frame, text = 'System Update', width = 25, command=lambda:_thread.start_new_thread(self.update,())).grid()
        tk.Button(self.frame, text = 'Nutzer CSV einlesen', width = 25).grid()
        tk.Button(self.frame, text = 'Passwort für Einstellungen ändern', width = 25).grid()
        tk.Button(self.frame, text = 'Systemlink herstellen', width = 25).grid()
        self.frame.grid()

    def update(self):
        os.system('sudo apt-get update -y')
        os.system('sudo apt-get upgrade -y')


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
        #check if pwd is correct
        if len(self.passwd) == 4 and self.passwd=="0815":
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
                self.lastdevice = str(device)[:61]
                self.newWindow = tk.Toplevel(self.master)
                self.app = CheckAdminPass(self.newWindow)

if __name__ == '__main__':
    root = tk.Tk()
    app = MainGui(root)
    _thread.start_new_thread( CheckforUsb, (root, ) )

    root.mainloop()
