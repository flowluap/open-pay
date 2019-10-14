# Open-Pay

## Getting started

Zuerst werden die Displaytreiber installiert:
```
sudo rm -rf LCD-show 
git clone https://github.com/goodtft/LCD-show.git 
chmod -R 755 LCD-show 
cd LCD-show/
sudo ./LCD35-show
```
Nach einem Reboot funktioniert das Touch-display

```
git clone https://github.com/flowluap/open-pay.git 
cd open-pay
#über ssh muss noch das richtige Display gewählt werden
export DISPLAY=:0.0
python3 guy.py

```
Ab diesem Zeitpunkt kann Open-Pay im vollen Umfang genutzt werden.
Um Open-Pay in einer Art Kioskmodus laufen zu lassen, habe ich mich dazu entschieden *nodm (einen minimalistischen Displaymanager) und openbox* zu verwenden, um einen möglichst schnellen Start zu erlauben.

```
sudo apt-get -y install nodm

# nodm config bearbeiten
sudo sed -i -e "s/NODM_ENABLED=false/NODM_ENABLED=true/" -e "s/NODM_USER=root/NODM_USER=pi/" \
  /etc/default/nodm

#Xsession Datei erstellen
printf "%s\n" \
  "#!/usr/bin/env bash" \
  "exec openbox-session &" \
  "while true; do" \
  "  python3 $PWD/open-pay/gui.py" \
  "done" \
  > /home/pi/.xsession
```
Dann werden noch die Bootkonfiurationen angepasst, sodass der Bootscreen klar bleibt:

```
#sudo nano /boot/cmdline.txt

console=tty1 --> console=tty3
loglevel=3
logo.nologo
```
```
#sudo nano /boot/config.txt

disable_splash=1
```
## Todos

  - [x] SQL Lite Merge (lastchanged attribute db for row)
  - [x] Main functionality (pay, get money)
  - [ ] Enable / Disable DHCP -->Button grey out Update
  - [ ] DB sync

  - [x] card add to kid && lost
  - [x] History file
  - [ ] sync history file
  - [x] All Kids list view

  - [ ] Export DB
  - [ ] show IP 
  
  ## Authors

* **Paul Wolf** - *Initial work* - 


