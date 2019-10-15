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
python3 gui.py

```
Auf dem Pi wird Maria DB genutz. Falls das **Netlink Feature** genutzt werden soll, muss in /etc/mysql/mariadb.conf.d/50-server.cnf die *bind_address=0.0.0.0* gesetzt werden. Außerdem muss der root Nutzer entsprechend angepasst werden. Für ein System, das über ein externes Netzwerk erreichbar ist, sollte diese Konfiguration nicht genutzt werden. Da hier aber nur Peer2Peer, oder in einem eigenen Netz kommuniziert wird, erachte ich das als vernachlässigbar.
```
GRANT ALL PRIVILEGES ON *.* TO 'root'@'10.0.0.%' IDENTIFIED BY '' WITH GRANT OPTION;
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

## Anleitung

### Einrichtung

Wenn Open-Pay auf dem System läuft, muss eine Nutzerdatenbank erstellt werden. Das geschieht über einen **CSV Import**. Hierbei ist es wichtig, dass das CSV Sheet mit **Kommata getrennt, utf-8 encoded** und die Spalten **"name" und "nachname"** besitzt. Die Spalten müssen genau so heißen, sodass die Software richtig importieren kann.
Um das zu erleichtern gibt es die Möglichkeit eine **leere CSV** mit diesen Anforderunge auf einen USB Stick zu laden:

```
Immmer wenn ein USB Gerät eingesteckt wird, wird es als /dev/sda in /media/sda gemountet.
Dabei öffnet sich ein Eingabefenster, in das man einen 4-stelligen PIN eingeben muss (default 0816).
Hier öffnen sich dann die Einstellungen, unter denen auch dieser Code geändert werden kann.
```

### Updaten

Der Pi wird zum Updaten *sudo apt-get update -y && sudo apt-get upgrade -y* an ein LAN angeschlossen. In den Einstellungen wird von "Statische IP" zu "DHCP" gewechselt. Der PI kann vom DHCP aus dem LAN nun eine IP Adresse beziehen und seine Updates aus dem Internet herunterladen. Bei jedem Neustart des Programmes wird die IP Adresse auf statisch umgestellt *10.0.0.1/24*, sodass ein Netzwerklink zwischen mehreren Geräten erfolgen kann.
**Edit:** Die Konfiguration "Statische IP" nutzt nur eine Statische IP als Fallback, falls kein DHCP verfügbar ist (was Peer2Peer ja der Fall ist). Sollte sich im Statischen Modus ein DHCP melden, wird dessen IP angenommen. Der Modus "DHCP" löscht in /etc/dhcpdc.conf den Fallback Teil von eth0 vollständig. (Siehe .env Datei NO_DHCP_CONFIG und DHCP_CONFIG)

## Going further
### Klonen von SD Karten, um mehrere Geräte einzusetzten:
Mit dd kann man unter OSX und Linux ein Image einer SD Karte erstellen und dieses auf eine Karte gleicher Größe wieder entpacken. (kleiner klappt nicht und bei einer größeren Karte müsste man die Partitionierung anpassen)
```
#In einer Shell (um den Namen des Gerätes z.B /dev/sda herauszufinden):
fdisk -l 
```
Dann das Image erstellen
```
sudo dd bs=4M if=/dev/{Gerät z.B. sda} | gzip > image.gz
```
Das Image auf eine SD Karte entpacken:
```
gzip -dc image.gz | sudo dd bs=4M of=/dev/{Gerät z.B. sda}
```
Sollte das Gerät im Linkmodus verwendert werden, empfiehlt es sich in der **.env Datei in Zeile 3 und 33** die IP-Adresse im Class-A 10.0.0.0/24 Netwerkraum fortzuführen.
## Todos



  - [x] DB sync
  - [x] change password
  - [x] sync history file
  - [x] Enable / Disable DHCP -->Button grey out Update
  - [x] SQL Lite Merge (lastchanged attribute db for row)
  - [x] Main functionality (pay, get money)
  - [x] card add to kid && lost
  - [x] History file
  - [x] All Kids list view
  - [x] Export DB
  - [x] show IP

## Authors

* **Paul Wolf** - *Initial work* -
