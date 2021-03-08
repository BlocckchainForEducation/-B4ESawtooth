import json

from sawtooth_sdk.processor.exceptions import InvalidTransaction

from processor.b4e_tp.handler.actor_handler import _check_is_valid_actor
from protobuf.b4e_protobuf import actor_pb2
from protobuf.b4e_protobuf import record_pb2
from protobuf.b4e_protobuf import payload_pb2
from protobuf.b4e_protobuf import voting_pb2
from protobuf.b4e_protobuf import class_pb2
from protobuf.b4e_protobuf import portfolio_pb2

from processor.b4e_tp.handler import time_handler


def create_record(state, public_key, transaction_id, payload):
    actor = state.get_actor(public_key)
    _check_is_valid_actor(actor)
    record_id = payload.data.record_id
    owner_public_key = payload.data.owner_public_key
    manager_public_key = payload.data.manager_public_key

    if state.get_record(record_id, owner_public_key, manager_public_key):
        raise InvalidTransaction("Record has been existed")
    if payload.data.record_type != payload_pb2.OTHER:
        raise InvalidTransaction("Only can create record with type OTHER")

    record_type = _get_record_type(payload.data.record_type)
    _create_record_with_type(state, transaction_id, payload, record_type)


def _create_record_with_type(state, transaction_id, payload, record_type):
    record_data = record_pb2.Record.RecordData(portfolio_id=payload.data.portfolio_id,
                                               cipher=payload.data.cipher,
                                               hash=payload.data.hash,
                                               record_status=record_pb2.Record.CREATED,
                                               timestamp=payload.timestamp,
                                               transaction_id=transaction_id)
    record = record_pb2.Record(owner_public_key=payload.data.owner_public_key,
                               manager_public_key=payload.data.manager_public_key,
                               issuer_public_key=payload.data.issuer_public_key,
                               record_id=payload.data.record_id,
                               record_type=record_type,
                               versions=[record_data])

    state.set_record(payload.data.record_id, record)


def _get_record_type(i):
    switcher = {
        payload_pb2.CERTIFICATE: record_pb2.Record.CERTIFICATE,
        payload_pb2.SUBJECT: record_pb2.Record.SUBJECT,
        payload_pb2.OTHER: record_pb2.Record.OTHER
    }
    return switcher.get(i)


def create_cert(state, public_key, transaction_id, payload):
    actor = state.get_actor(public_key)
    _check_is_valid_actor(actor)
    record_id = payload.data.record_id
    owner_public_key = payload.data.owner_public_key
    manager_public_key = payload.data.manager_public_key

    if state.get_record(record_id, owner_public_key, manager_public_key):
        raise InvalidTransaction("Record has been existed")

    if actor.role != actor_pb2.Actor.INSTITUTION:
        raise InvalidTransaction("Just Institution can't create certificate")

    portfolio = state.get_portfolio(id=payload.data.portfolio_id,
                                    owner_public_key=owner_public_key,
                                    manager_public_key=manager_public_key)
    if not portfolio or portfolio.portfolio_data[-1]:
        raise InvalidTransaction("Invalid edu program")
    portfolio_data = portfolio.portfolio_data[-1]
    if portfolio_data.type != portfolio_pb2.Portfolio.EDU_PROGRAM:
        raise InvalidTransaction("Invalid portfolio type")

    edu_program_data = json.loads(portfolio_data.data)
    if (not edu_program_data.get("currentCredit")) or (
            not edu_program_data.get("startTimestamp")) or (not edu_program_data.get("latestTimestamp")):
        raise InvalidTransaction("Not enough condition ")
    if int(edu_program_data.get("currentCredit")) < int(edu_program_data.get("totalCredit")):
        raise InvalidTransaction("Not enough credit")
    start_year = time_handler.timestamp_to_datetime(int(edu_program_data.get("startTimestamp"))).year
    latest_year = time_handler.timestamp_to_datetime(int(edu_program_data.get("latestTimestamp"))).year
    duration = latest_year - start_year

    if duration < int(edu_program_data.get("minYear")):
        raise InvalidTransaction("Not reach min year")
    if duration > int(edu_program_data.get("maxYear")):
        raise InvalidTransaction("Exceed max year")

    record_type = record_pb2.Record.CERTIFICATE
    _create_record_with_type(state, transaction_id, payload, record_type)


def create_subject(state, public_key, transaction_id, payload):
    actor = state.get_actor(public_key)
    _check_is_valid_actor(actor)
    record_id = payload.data.record_id
    owner_public_key = payload.data.owner_public_key
    manager_public_key = payload.data.manager_public_key

    if state.get_record(record_id, owner_public_key, manager_public_key):
        raise InvalidTransaction("Record has been existed")

    class_ = state.get_class(payload.data.record_id, manager_public_key)
    if not class_:
        raise InvalidTransaction("Class doesn't exist!")

    if public_key != class_.teacher_public_key and public_key != class_.edu_officer_public_key:
        raise InvalidTransaction("Invalid issuer for this class")
    portfolio = state.get_portfolio(id=payload.data.portfolio_id,
                                    owner_public_key=owner_public_key,
                                    manager_public_key=manager_public_key)

    if not portfolio or portfolio.portfolio_data[-1]:
        raise InvalidTransaction("Invalid edu program")
    portfolio_data = portfolio.portfolio_data[-1]
    if portfolio_data.type != portfolio_pb2.Portfolio.EDU_PROGRAM:
        raise InvalidTransaction("Invalid portfolio type")
    edu_program_data = json.loads(portfolio_data.data)
    if not edu_program_data.get('currentCredit'):
        edu_program_data['currentCredit'] = class_.credit
    else:
        edu_program_data['currentCredit'] += class_.credit

    if not edu_program_data.get("startTimestamp"):
        edu_program_data["startTimestamp"] = payload.timestamp
    else:
        edu_program_data["latestTimestamp"] = payload.timestamp

    record_type = record_pb2.Record.SUBJECT
    _create_record_with_type(state, transaction_id, payload, record_type)

    state.update_portfolio_data(payload.data.portfolio_id, owner_public_key, manager_public_key)


def update_record(state, public_key, transaction_id, payload):
    pass


def modify_subject(state, public_key, transaction_id, payload):
    pass


def modify_cert(state, public_key, transaction_id, payload):
    pass


def revoke_cert(state, public_key, transaction_id, payload):
    pass


def reactive_cert(state, public_key, transaction_id, payload):
    pass
