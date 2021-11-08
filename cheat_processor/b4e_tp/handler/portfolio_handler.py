import logging

from sawtooth_sdk.processor.exceptions import InvalidTransaction

from processor.b4e_tp.handler.actor_handler import _check_is_valid_actor
from protobuf.b4e_protobuf import actor_pb2
from protobuf.b4e_protobuf import record_pb2
from protobuf.b4e_protobuf import payload_pb2
from protobuf.b4e_protobuf import voting_pb2
from protobuf.b4e_protobuf import class_pb2
from protobuf.b4e_protobuf import portfolio_pb2

import json

LOGGER = logging.getLogger(__name__)


def create_portfolio(state, public_key, transaction_id, payload):
    pass


def create_edu_program(state, public_key, transaction_id, payload):
    owner_public_key = payload.data.owner_public_key
    edu_id = payload.data.id
    portfolio_type = portfolio_pb2.Portfolio.EDU_PROGRAM
    data = payload.data.data

    institution = state.get_actor(public_key)
    if _check_is_valid_actor(institution):
        raise InvalidTransaction("Invalid institution")

    if institution.role != actor_pb2.Actor.INSTITUTION:
        raise InvalidTransaction("Invalid signer!")

    if state.get_portfolio(edu_id, owner_public_key, public_key):
        raise InvalidTransaction("Edu program has been existed")

    if not _check_data_edu_program(data):
        raise InvalidTransaction("Invalid fields on edu program")

    _check_type_edu_program_field(data)

    portfolio_data = portfolio_pb2.Portfolio.PortfolioData(portfolio_type=portfolio_type,
                                                           data=data,
                                                           timestamp=payload.timestamp,
                                                           transaction_id=transaction_id)
    portfolio = portfolio_pb2.Portfolio(owner_public_key=owner_public_key, manager_public_key=public_key,
                                        id=edu_id,
                                        portfolio_data=[portfolio_data],
                                        timestamp=payload.timestamp,
                                        transaction_id=transaction_id)
    state.create_portfolio(portfolio)


def _check_data_edu_program(data):
    try:
        edu_program_data = json.loads(data)
        required_fields = ['eduProgramId', 'name', "totalCredit", "minYear", "maxYear"]
        return _validate_fields(required_fields, edu_program_data)
    except Exception as e:
        print(e)
        return False


def _check_type_edu_program_field(data):
    edu_program_data = json.loads(data)
    fields = ["totalCredit", "minYear", "maxYear"]
    for field in fields:
        if type(edu_program_data.get(field)) != int:
            raise InvalidTransaction(field + " must be int type")


def _validate_fields(required_fields, data):
    for field in required_fields:
        if data.get(field) is None:
            return False
    return True
