# led_alert

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Raspberry Pi](https://img.shields.io/badge/-RaspberryPi-C51A4A?style=for-the-badge&logo=Raspberry-Pi)
[![Licence](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](./LICENSE)

[![Pylint](https://github.com/TheGoatNote/led_alert/actions/workflows/pylint.yml/badge.svg)](https://github.com/TheGoatNote/led_alert/actions/workflows/pylint.yml)

## To Begin

The purpose of this repo is to be able to install a monitoring system plugs with Opsgenie (for example)
One raspberry pi will manage a led which will switch on when a hight alert is comming
The other one will display the alert message

### Prerequisite

- Two Raspberry pi 0w with Raspbian lite on it
- Jumpers
- One red led
- One 2.13 E-Paper
- It would be useful to do a git clone of waveshare library and to get the directory 'lib' and 'pic' for Raspi Screen
```
git clone https://github.com/waveshare/e-Paper
```

### Installation (on each raspberry pi)
- We will install mosquitto package
```
sudo apt-get install mosquitto mosquitto-clients
```

- Clone the directory you need (screenOps for E_paper and ledOps for the led)

- We create a venv and install our python packages
```
python3 -m venv venv
source venv/bin/activate
python3 install -r requirement.txt
```
- Now we have our file we can create a systemd service to be start at boot
```
sudo cp mqtt.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start mqtt.service
sudo systemctl enable mqtt.service
```
- On your own computer create a venv and install requirement
- You can now create a cron to call opsgenie_led.py each time you want

### Tips
- A generic .env file is create on this repo, you have to edit it with your own informations
- If you don't know how to put your led on your Pi you can use this [link](https://raspberry-pi.fr/led-raspberry-pi/)
