import json
import logging

from sawtooth_sdk.processor.exceptions import InvalidTransaction

from processor.b4e_tp.handler.actor_handler import _check_is_valid_actor
from protobuf.b4e_protobuf import actor_pb2
from protobuf.b4e_protobuf import record_pb2
from protobuf.b4e_protobuf import payload_pb2
from protobuf.b4e_protobuf import portfolio_pb2

from processor.b4e_tp.handler import time_handler

logger = logging.getLogger("Record Handler")


def create_record(state, public_key, transaction_id, payload):
    actor = state.get_actor(public_key)
    _check_is_valid_actor(actor)
    record_id = payload.data.record_id

    logger.info(f"Create record {record_id}")

    owner_public_key = payload.data.owner_public_key
    manager_public_key = payload.data.manager_public_key

    if state.get_record(record_id, owner_public_key, manager_public_key):
        raise InvalidTransaction("Record has been existed")
    if payload.data.record_type != payload_pb2.OTHER:
        raise InvalidTransaction("Only can create record with type OTHER")

    record_type = _get_record_type(payload.data.record_type)
    _create_record_with_type(state, transaction_id, payload, record_type)


def _create_record_with_type(state, transaction_id, payload, record_type):
    logger.info(f'Creating record {record_type}')
    record_data = record_pb2.Record.RecordData(portfolio_id=payload.data.portfolio_id,
                                               cipher=payload.data.cipher,
                                               hash=payload.data.hash,
                                               record_status=record_pb2.Record.CREATED,
                                               timestamp=payload.timestamp,
                                               transaction_id=transaction_id)
    record = record_pb2.Record(owner_public_key=payload.data.owner_public_key,
                               manager_public_key=payload.data.manager_public_key,
                               record_id=payload.data.record_id,
                               record_type=record_type,
                               versions=[record_data])

    state.set_record(record)


def _get_record_type(i):
    switcher = {
        payload_pb2.CERTIFICATE: record_pb2.Record.CERTIFICATE,
        payload_pb2.SUBJECT: record_pb2.Record.SUBJECT,
        payload_pb2.OTHER: record_pb2.Record.OTHER
    }
    return switcher.get(i)


def create_cert(state, public_key, transaction_id, payload):
    logger.info(f"Create cert")
    actor = state.get_actor(public_key)
    _check_is_valid_actor(actor)
    record_id = payload.data.record_id
    owner_public_key = payload.data.owner_public_key
    manager_public_key = payload.data.manager_public_key

    if state.get_record(record_id, owner_public_key, manager_public_key):
        raise InvalidTransaction("Record has been existed")

    if actor.role != actor_pb2.Actor.INSTITUTION:
        raise InvalidTransaction("Just Institution can create certificate")

    portfolio = state.get_portfolio(id=payload.data.portfolio_id,
                                    owner_public_key=owner_public_key,
                                    manager_public_key=manager_public_key)
    if not portfolio or not portfolio.portfolio_data[-1]:
        raise InvalidTransaction("Invalid edu program")
    portfolio_data = portfolio.portfolio_data[-1]
    if portfolio_data.portfolio_type != portfolio_pb2.Portfolio.EDU_PROGRAM:
        raise InvalidTransaction("Invalid portfolio type")

    data = portfolio_data.data

    edu_program_data = json.loads(data)

    logger.info(f"Checking educational program data ... ")

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

    logger.info(f"Create subject {record_id}")

    if state.get_record(record_id, owner_public_key, manager_public_key):
        raise InvalidTransaction("Record has been existed")

    class_ = state.get_class(payload.data.record_id, manager_public_key)
    if not class_:
        raise InvalidTransaction("Class doesn't exist!")

    if public_key != class_.teacher_public_key:
        raise InvalidTransaction("Invalid issuer for this class")

    if owner_public_key not in class_.student_public_keys:
        raise InvalidTransaction("Invalid issuer for this student in the class")

    portfolio = state.get_portfolio(id=payload.data.portfolio_id,
                                    owner_public_key=owner_public_key,
                                    manager_public_key=manager_public_key)
    if not portfolio or not portfolio.portfolio_data[-1]:
        raise InvalidTransaction("Invalid edu program")
    portfolio_data = portfolio.portfolio_data[-1]
    if portfolio_data.portfolio_type != portfolio_pb2.Portfolio.EDU_PROGRAM:
        raise InvalidTransaction("Invalid portfolio type")
    edu_program_data = json.loads(portfolio_data.data)

    logger.info(f"Checking educational program data")

    if not edu_program_data.get('currentCredit'):
        edu_program_data['currentCredit'] = class_.credit
    else:
        edu_program_data['currentCredit'] += class_.credit

    if not edu_program_data.get("startTimestamp"):
        edu_program_data["startTimestamp"] = payload.timestamp
    if not edu_program_data.get("latestTimestamp"):
        edu_program_data["latestTimestamp"] = payload.timestamp
    elif edu_program_data.get("latestTimestamp") < payload.timestamp:
        edu_program_data["latestTimestamp"] = payload.timestamp

    record_type = record_pb2.Record.SUBJECT
    _create_record_with_type(state, transaction_id, payload, record_type)

    state.update_portfolio_data(payload.data.portfolio_id, owner_public_key, manager_public_key,
                                json.dumps(edu_program_data))


def _get_record_status(i):
    switcher = {
        payload_pb2.CREATED: record_pb2.Record.CREATED,
        payload_pb2.REVOKED: record_pb2.Record.REVOKED,
        payload_pb2.REACTIVATED: record_pb2.Record.REACTIVATED
    }
    return switcher.get(i)


def update_record(state, public_key, transaction_id, payload):
    actor = state.get_actor(public_key)
    _check_is_valid_actor(actor)
    record_id = payload.data.record_id

    logger.info(f"Updating record {record_id}")

    owner_public_key = payload.data.owner_public_key
    manager_public_key = payload.data.manager_public_key
    record = state.get_record(record_id, owner_public_key, manager_public_key)
    _check_modify_permission(state, record, payload, manager_public_key, public_key)

    status = _get_record_status(payload.data.status)
    state.update_record(record_id, owner_public_key, manager_public_key, payload.data.cipher,
                        payload.data.hash, status,
                        payload.timestamp, transaction_id)


def _check_modify_permission(state, record, payload, manager_public_key, public_key):
    # return True
    if not record:
        raise InvalidTransaction("Record doesn't exist")

    class_ = state.get_class(payload.data.record_id, manager_public_key)

    if class_:
        if class_.teacher_public_key != public_key:
            raise InvalidTransaction("Invalid permission")
    else:
        raise InvalidTransaction("Class doesn't exit ")


def modify_record(state, public_key, transaction_id, payload):
    actor = state.get_actor(public_key)
    _check_is_valid_actor(actor)
    record_id = payload.data.record_id
    owner_public_key = payload.data.owner_public_key
    manager_public_key = payload.data.manager_public_key
    record = state.get_record(record_id, owner_public_key, manager_public_key)
    _check_modify_permission(state, record, payload, manager_public_key, public_key)

    state.modify_record(record_id, owner_public_key, manager_public_key, payload.data.cipher,
                        payload.data.hash,
                        payload.timestamp, transaction_id)


def modify_subject(state, public_key, transaction_id, payload):
    modify_record(state, public_key, transaction_id, payload)


def modify_cert(state, public_key, transaction_id, payload):
    modify_record(state, public_key, transaction_id, payload)


def update_status(state, public_key, transaction_id, payload, status):
    actor = state.get_actor(public_key)
    _check_is_valid_actor(actor)
    record_id = payload.data.record_id
    owner_public_key = payload.data.owner_public_key
    manager_public_key = public_key
    record = state.get_record(record_id, owner_public_key, manager_public_key)
    _check_modify_permission(state, record, payload, manager_public_key, public_key)

    state.update_status_record(record_id, owner_public_key,
                               manager_public_key, status,
                               payload.timestamp, transaction_id)


def revoke_cert(state, public_key, transaction_id, payload):
    update_status(state, public_key, transaction_id, payload, record_pb2.Record.REVOKED)


def reactive_cert(state, public_key, transaction_id, payload):
    update_status(state, public_key, transaction_id, payload, record_pb2.Record.REACTIVATED)
