import logging

from sawtooth_sdk.processor.exceptions import InvalidTransaction
from protobuf.b4e_protobuf import actor_pb2
from protobuf.b4e_protobuf import voting_pb2

logger = logging.getLogger("Actor handler")

list_ministry_public_key = []
with open("list_ministry_public_key") as fp:
    for line in fp:
        list_ministry_public_key.append(line.strip())


def _check_is_valid_actor(actor):
    if not actor:
        raise InvalidTransaction(f"Actor doesn't exist : {actor}")
    if actor.profile[-1].status != actor_pb2.Actor.ACTIVE:
        raise InvalidTransaction(f"Actor is not active {actor}")


def _create_actor(state, public_key, transaction_id, manager_public_key, status, payload, role):
    logger.info(f"Create actor with: {public_key}")
    if state.get_actor(public_key):
        raise InvalidTransaction("Actor existed!")
    actor_public_key = public_key
    actor_id = payload.data.id

    profile = actor_pb2.Actor.Profile(data=payload.data.data,
                                      status=status,
                                      transaction_id=transaction_id,
                                      timestamp=payload.timestamp
                                      )
    actor = actor_pb2.Actor(actor_public_key=actor_public_key,
                            manager_public_key=manager_public_key,
                            id=actor_id,
                            role=role,
                            profile=[profile],
                            transaction_id=transaction_id,
                            timestamp=payload.timestamp)
    logger.info(f"Set actor state")
    state.set_actor(actor, public_key)
    logger.info(f"Created actor")


def create_actor(state, public_key, transaction_id, payload):
    status = actor_pb2.Actor.ACTIVE
    role = actor_pb2.Actor.OTHER
    _create_actor(state, public_key, transaction_id, public_key, status, payload, role)


def create_institution(state, public_key, transaction_id, payload):
    logger.info(f"Create institution {public_key} with voting")
    _create_actor(state=state,
                  public_key=public_key,
                  transaction_id=transaction_id,
                  manager_public_key=public_key,
                  status=actor_pb2.Actor.WAITING,
                  payload=payload,
                  role=actor_pb2.Actor.INSTITUTION)

    voting = voting_pb2.Voting(publisher_public_key=public_key,
                               elector_public_key=public_key,
                               vote_type=voting_pb2.Voting.ACTIVE,
                               vote=[],
                               vote_result=voting_pb2.Voting.UNKNOWN,
                               close_vote_timestamp=0,
                               timestamp=payload.timestamp,
                               transaction_id=transaction_id)
    logger.info("Create voting")
    state.set_voting(voting, public_key)
    logger.info("Voting created")


def create_teacher(state, public_key, transaction_id, payload):
    logger.info(f"Create teacher by {public_key}")
    institution = state.get_actor(public_key)
    _check_is_valid_actor(institution)

    if institution.role != actor_pb2.Actor.INSTITUTION:
        raise InvalidTransaction("Invalid signer!")

    _create_actor(state=state,
                  public_key=payload.data.teacher_public_key,
                  transaction_id=transaction_id,
                  manager_public_key=public_key,
                  status=actor_pb2.Actor.ACTIVE,
                  payload=payload,
                  role=actor_pb2.Actor.TEACHER)


def update_actor_profile(state, public_key, transaction_id, payload):
    logger.info(f"Update actor {public_key}")
    actor = state.get_actor(public_key)
    _check_is_valid_actor(actor)

    if actor.actor_public_key != public_key:
        raise InvalidTransaction("Illegal")

    state.update_actor_profile(public_key, payload.data.data, payload.timestamp, transaction_id)


def reject_institution(state, public_key, transaction_id, payload):
    logger.info(f"Reject institution {public_key}")
    if public_key in list_ministry_public_key:
        institution = state.get_actor(public_key)
        _check_is_valid_actor(institution)

        if institution.role != actor_pb2.Actor.INSTITUTION:
            raise InvalidTransaction("Actor is not a institution!")
        state.set_reject_actor(institution.actor_public_key, payload.timestamp, transaction_id)


def active_institution(state, public_key, transaction_id, payload):
    logger.info(f"Active institution {public_key}")
    if public_key in list_ministry_public_key:
        institution = state.get_actor(public_key)
        _check_is_valid_actor(institution)

        if institution.role != actor_pb2.Actor.INSTITUTION:
            raise InvalidTransaction("Actor is not a institution!")
        state.set_active_actor(institution.actor_public_key, payload.timestamp, transaction_id)
