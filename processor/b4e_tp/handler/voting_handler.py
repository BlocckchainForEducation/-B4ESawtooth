from sawtooth_sdk.processor.exceptions import InvalidTransaction
from protobuf.b4e_protobuf import actor_pb2
from protobuf.b4e_protobuf import record_pb2
from protobuf.b4e_protobuf import payload_pb2
from protobuf.b4e_protobuf import voting_pb2
from protobuf.b4e_protobuf import class_pb2


import logging

LOGGER = logging.getLogger(__name__)

list_ministry_public_key = []
with open("list_ministry_public_key") as fp:
    for line in fp:
        list_ministry_public_key.append(line.strip())

VOTE_RATE = 0.5


def create_voting(state, public_key, transaction_id, payload):
    pass


def vote(state, public_key, transaction_id, payload):
    pass
