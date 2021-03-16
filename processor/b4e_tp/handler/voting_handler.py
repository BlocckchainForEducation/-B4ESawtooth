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

    timestamp = payload.timestamp
    actor_vote = voting_pb2.Voting.Vote(issuer_public_key=public_key, accept=payload.data.accept,
                                        timestamp=payload.timestamp, transaction_id=transaction_id)
    if public_key in list_ministry_public_key:

        if payload.data.accept:
            close_vote_timestamp = payload.timestamp
            vote_result = voting_pb2.Voting.WIN
            if voting.vote_type == voting_pb2.Voting.ACTIVE:
                state.set_active_actor(payload.data.elector_public_key, timestamp, transaction_id)
                state.add_one_b4e_environment(transaction_id=transaction_id)
            elif voting.vote_type == voting_pb2.Voting.REJECT:
                state.set_reject_actor(payload.data.elector_public_key, timestamp, transaction_id)
                state.subtract_one_b4e_environment(transaction_id=transaction_id)
        else:
            if voting.vote_type == voting_pb2.Voting.REJECT:
                state.set_active_actor(payload.data.elector_public_key, timestamp, transaction_id)
                state.subtract_one_b4e_environment(transaction_id=transaction_id)
            elif voting.vote_type == voting_pb2.Voting.ACTIVE:
                state.set_reject_actor(payload.data.elector_public_key, timestamp, transaction_id)
                state.add_one_b4e_environment(transaction_id=transaction_id)

        state.update_voting(payload.data.elector_public_key, vote_result,
                            actor_vote, timestamp=close_vote_timestamp)

        return

    actor = state.get_actor(public_key)
    _check_is_valid_actor(actor)
    if actor.role != actor_pb2.Actor.INSTITUTION:
        raise InvalidTransaction("Actor must be INSTITUTION")

    env = state.get_b4e_environment()
    election = voting.vote
    accept = 0
    reject = 0
    total = env.institution_number + 1
    # count accept and reject voted
    for voted in election:
        if voted.accept:
            accept += 1
        else:
            reject += 1
    # add voted
    if payload.data.accept:
        accept += 1
    else:
        reject += 1

        # check for close vote
    if accept / total > VOTE_RATE:
        vote_result = voting_pb2.Voting.WIN
        state.update_voting(payload.data.elector_public_key, vote_result,
                            actor_vote, timestamp=payload.timestamp)
        if voting.vote_type == voting_pb2.Voting.ACTIVE:
            state.set_active_actor(payload.data.elector_public_key, timestamp, transaction_id)
        elif voting.vote_type == voting_pb2.Voting.REJECT:
            state.set_reject_actor(payload.data.elector_public_key, timestamp, transaction_id)
        return

    if reject / total > VOTE_RATE:
        vote_result = voting_pb2.Voting.LOSE
        state.update_voting(payload.data.elector_public_key, vote_result,
                            actor_vote, timestamp=payload.timestamp)
        if voting.vote_type == voting_pb2.Voting.REJECT:
            state.set_active_actor(payload.data.elector_public_key, timestamp, transaction_id)
        elif voting.vote_type == voting_pb2.Voting.ACTIVE:
            state.set_reject_actor(payload.data.elector_public_key, timestamp, transaction_id)
        return
        #
    vote_result = voting_pb2.Voting.UNKNOWN
    state.update_voting(payload.data.elector_public_key, vote_result,
                        actor_vote, timestamp=close_vote_timestamp)
