import logging
import time

import requests

LOGGER = logging.getLogger(__name__)


def request_to_host(data, url_name):
    from config.config import SubscriberConfig
    HOST = SubscriberConfig.HOST
    PORT = SubscriberConfig.PORT
    PROTOCOL = SubscriberConfig.PROTOCOL
    URL = {
        "registration": PROTOCOL + "://" + HOST + ":" + PORT + "/events/registration",
        "vote": PROTOCOL + "://" + HOST + ":" + PORT + "/events/vote",
        "vote_close": PROTOCOL + "://" + HOST + ":" + PORT + "/events/vote-closed",

    }
    LOGGER.info(URL.get(url_name))

    while True:
        response = requests.post(URL.get(url_name), json=data)
        if response.status_code == 200:
            return
        else:
            time.sleep(1)


def request_registration(data):
    request_to_host(data, "registration")


def request_vote(data):
    request_to_host(data, "vote")


def request_vote_close(data):
    request_to_host(data, "vote_close")
