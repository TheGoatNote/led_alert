"""
This script has to be set on the Pi with the led
"""
import logging
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
LED = 7
GPIO.setup(LED, GPIO.OUT)

MQTT_SERVER = "localhost"
MQTT_PATH = "alerting"

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

def on_connect(client_mqtt, userdata, flags, result_code):
    """
    Connexion to mqtt broker
    """
    logging.info("Connected with result code %s", result_code)
    client_mqtt.subscribe(MQTT_PATH)

def on_message(client_mqtt, userdata, msg):
    """
    Received message, if UP raise an alert, if DOWN display switch on the light
    """
    logging.info("%s %s", msg.topic, msg.payload)
    msg.payload = msg.payload.decode("utf-8")
    if msg.payload == "UP":
        GPIO.output(LED, GPIO.HIGH)
    else:
        GPIO.output(LED, GPIO.LOW)
client_mqtt = mqtt.Client()
client_mqtt.on_connect = on_connect
client_mqtt.on_message = on_message

client_mqtt.connect(MQTT_SERVER, 1883, 60)

client_mqtt.loop_forever()
