import base64
import json
import logging
import time
from requests.exceptions import Timeout

import requests

from addressing.b4e_addressing import addresser
from config.config import SubscriberConfig, SawtoothConfig

from subscriber_b4e.b4e_subscriber.decoding import deserialize_data

LOGGER = logging.getLogger(__name__)


def request_to_host(data, url_name):
    HOST_URL = SubscriberConfig.HOST_URL
    URL = {
        "registration": HOST_URL + "/events/registration",
        "vote": HOST_URL + "/events/vote",
        "vote_close": HOST_URL + "/events/vote-closed",

    }
    LOGGER.info(URL.get(url_name))

    while True:

        try:
            response = requests.post(URL.get(url_name), json=data, timeout=2)
        except Timeout:
            continue
        else:
            if response.status_code == 200:
                return
            else:
                time.sleep(2)


def request_on_actor(data):
    pass


def request_on_voting(data):
    # for registration
    if len(data.get("vote")) < 1:
        registration = get_actor_from_state(data.get('elector_public_key'))
        profile = registration.get("profile")[-1].get("data")
        request_registration({"profile": json.loads(profile)})
    # for vote
    else:
        vote = data.get("vote")[-1]
        reformat_data = {"publicKey": vote.get("issuer_public_key"),
                         "requesterPublicKey": data.get("elector_public_key"),
                         "decision": _decision_type(vote.get('accept')),
                         "timestamp": vote.get("timestamp"),
                         "transaction_id": vote.get("transaction_id")}
        request_vote(reformat_data)

        # for vote close
        if data.get("close_vote_timestamp") > 0:
            close_vote_data = {
                "requesterPublicKey": data.get("elector_public_key"),
                "finalState": _vote_result_type(data.get("vote_result")),
                "timestamp": vote.get("timestamp"),
                "transaction_id": vote.get("transaction_id")
            }
            request_vote_close(close_vote_data)


def _decision_type(i):
    switch = {
        True: "accept",
        False: "decline"
    }
    return switch.get(i)


def _vote_result_type(i):
    switch = {
        "WIN": "accepted",
        "LOSE": "declined"
    }
    return switch.get(i)


def request_registration(data):
    request_to_host(data, "registration")


def request_vote(data):
    request_to_host(data, "vote")


def request_vote_close(data):
    request_to_host(data, "vote_close")


def get_actor_from_state(public_key):
    actor_public_key = addresser.get_actor_address(public_key=public_key)
    return get_state(actor_public_key)


def get_state(sawtooth_address):
    url = SawtoothConfig.REST_API + "/state/" + str(sawtooth_address)
    response = requests.get(url)
    if response.status_code == 200:
        try:
            state_dict = json.loads(response.content)
            payload_string = state_dict['data']
            data_type, data = deserialize_data(sawtooth_address, base64.b64decode(payload_string))
            return data[-1]

        except Exception as e:
            print("err:", e)
            return {'msg': "err"}
