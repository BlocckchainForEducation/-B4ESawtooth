from sawtooth_sdk.processor.exceptions import InvalidTransaction

from processor.b4e_tp.handler.actor_handler import _check_is_valid_actor
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
    permission = False

    if public_key in list_ministry_public_key:
        permission = True

    institution = state.get_actor(public_key)
    _check_is_valid_actor(institution)

    if institution.role == actor_pb2.Actor.INSTITUTION:
        permission = True

    if not permission:
        raise InvalidTransaction("Invalid permission")

    institution = state.get_actor(payload.data.elector_public_key)
    if not institution:
        raise InvalidTransaction("elector doesn't exist")

    voting = state.get_voting(payload.data.elector_public_key)
    if voting and voting.close_vote_timestamp == 0:
        raise InvalidTransaction("Voting is happening, can't open other one")

    voting = voting_pb2.Voting(publisher_public_key=public_key,
                               elector_public_key=public_key,
                               voteType=_get_voting_type(payload.data.voteType),
                               vote=[],
                               vote_result=voting_pb2.Voting.UNKNOWN,
                               close_vote_timestamp=0,
                               timestamp=payload.timestamp,
                               transaction_id=transaction_id)

    state.set_voting(voting, public_key)


def _get_voting_type(i):
    switch = {
        payload_pb2.ACTIVE: voting_pb2.Voting.ACTIVE,
        payload_pb2.REJECT: voting_pb2.Voting.REJECT
    }
    return switch(i)


def vote(state, public_key, transaction_id, payload):
    close_vote_timestamp = 0
    voting = state.get_voting(payload.data.elector_public_key)
    if not voting:
        raise InvalidTransaction("Voting doesn't exist")
    if voting.close_vote_timestamp > 0:
        raise InvalidTransaction("Voting has been closed")
    if public_key == voting.elector_public_key:
        raise InvalidTransaction("You can't vote for yourself")

    for vote in voting.vote:
        if vote.issuer_public_key == public_key:
            raise InvalidTransaction("Issuer has voted!")

    actor_vote = voting_pb2.Voting.Vote(issuer_public_key=public_key, accepted=payload.data.accepted,
                                        timestamp=payload.timestamp, transaction_id=transaction_id)
    if public_key in list_ministry_public_key:

        if payload.data.accepted:
            close_vote_timestamp = payload.timestamp
            vote_result = voting_pb2.Voting.WIN
            state.add_one_b4e_environment(transaction_id=transaction_id)
            if voting.accepted:
                state.set_active_actor(payload.data.elector_public_key)
            else:
                state.set_reject_actor(payload.data.elector_public_key)
        else:
            vote_result = voting_pb2.Voting.UNKNOWN

        state.update_voting(payload.data.elector_public_key, vote_result,
                            actor_vote, timestamp=close_vote_timestamp)

        return
