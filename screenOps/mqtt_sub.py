"""
This script has to be use on Pi Screen
"""
import logging
import os
import re
import sys
import time
import paho.mqtt.client as mqtt

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pic")
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "lib")
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in13_V2
from PIL import Image, ImageDraw, ImageFont

epd = epd2in13_V2.EPD()
epd.init(epd.FULL_UPDATE)
epd.Clear(0xFF)
image = Image.open(os.path.join(picdir, "2in13.bmp"))
font24 = ImageFont.truetype(os.path.join(picdir, "Font.ttc"), 12)
epd.display(epd.getbuffer(image))
time.sleep(2)

MQTT_SERVER_MESSAGE = "localhost"
MQTT_PATH_MESSAGE = "message"

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

def on_connect(client, userdata, flags, result_code):
    """
    Connexion to mqtt broker
    """
    logging.info("Connected with result code %s", result_code)

    client.subscribe(MQTT_PATH_MESSAGE)

def on_message(client, userdata, msg):
    """
    Received message, if UP raise an alert, if DOWN display image
    """
    logging.info("%s %s", msg.topic, msg.payload)
    msg.payload = msg.payload.decode("utf-8")
    if msg.payload == "DOWN":
        epd.display(epd.getbuffer(image))
        time.sleep(2)
    else:
        message_strip = re.split(r"\s{1,}", msg.payload.strip())
        node = message_strip[0]
        detail = message_strip[3]
        detail_strip = re.split(",", detail.strip())

        alert_image = Image.new("1", (epd.height, epd.width), 255)
        alert_draw = ImageDraw.Draw(alert_image)

        epd.init(epd.FULL_UPDATE)
        epd.displayPartBaseImage(epd.getbuffer(alert_image))

        epd.init(epd.PART_UPDATE)
        num = 0
        while True:
            alert_draw.text(
                (0, 0),
                f"{node} \n Detail : {detail_strip[0]}",
                font=font24,
                fill=0,
                align="left",
            )

            epd.display(epd.getbuffer(alert_image))

            num = num + 1
            if num == 10:
                break

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER_MESSAGE, 1883, 60)

client.loop_forever()
