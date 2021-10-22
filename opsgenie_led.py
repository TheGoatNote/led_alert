"""
This module will parse our monitoring to send alert to two brokers
One for switching on a led
One for displaying a message on a screen
"""
import logging
import os
from paho.mqtt import publish
from dotenv import load_dotenv
import requests

load_dotenv()
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
MQTT_SERVER_ALERTING = os.getenv('MQTT_SERVER_ALERTING')
MQTT_PATH_ALERTING = "alerting"

MQTT_SERVER_MESSAGE = os.getenv('MQTT_SERVER_MESSAGE')
MQTT_PATH_MESSAGE = "message"

URL = os.getenv('URL')
TOKEN = os.getenv('TOKEN')

def get_alert_list():
    """
    Get Opsgenie alert information except P4

    """
    logging.info("We get alert list from our monitoring")
    try:
        call_api = requests.get(f"{URL}", \
                   headers={'Authorization': f'GenieKey {TOKEN}'})
        return call_api.json()
    except requests.exceptions.RequestException as exc:
        return exc

def parse_return_data():
    """
    We parse the return, if empty send signal "DOWN" to the broker
    Else send "UP" and the message
    """
    logging.info("We search if we have bigs alerts")
    data_parser = get_alert_list()["data"]
    is_alerting = False
    if not data_parser:
        logging.info("Nothing to do, juste beautifuls flowers")
        publish.single(MQTT_PATH_ALERTING, "DOWN", hostname=MQTT_SERVER_ALERTING)
        publish.single(MQTT_PATH_MESSAGE, "DOWN", hostname=MQTT_SERVER_MESSAGE)

    else:
        is_alerting = True
        logging.info("Hum, ALARMA")
        for i in data_parser:
            message_alert = i['message']
            publish.single(MQTT_PATH_MESSAGE, f"{message_alert}", hostname=MQTT_SERVER_MESSAGE)
            publish.single(MQTT_PATH_ALERTING, "UP", hostname=MQTT_SERVER_ALERTING)
            break
    return is_alerting
if __name__ == '__main__':
    parse_return_data()
