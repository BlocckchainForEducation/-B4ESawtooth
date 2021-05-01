import json

from sawtooth_sdk.processor.exceptions import InvalidTransaction

from processor.b4e_tp.handler.actor_handler import _check_is_valid_actor
from protobuf.b4e_protobuf import payload_pb2
from protobuf.b4e_protobuf import actor_pb2
from protobuf.b4e_protobuf import job_pb2


def job_begin(state, public_key, transaction_id, payload):
    company = state.get_actor(public_key)
    _check_is_valid_actor(company)

    job_id = payload.data.job_id
    company_public_key = payload.data.company_public_key
    candidate_public_key = payload.data.candidate_public_key
    timestamp = payload.timestamp
    cipher = payload.data.cipher
    hash = payload.data.hash

    if company.role != actor_pb2.Actor.COMPANY:
        raise InvalidTransaction("Just Institution can create job")

    if state.get_job(job_id, company_public_key, candidate_public_key):
        raise InvalidTransaction("Job has been existed")

    start = job_pb2.Job.Start(timestamp=timestamp,
                              cipher=cipher,
                              hash=hash,
                              transaction_id=transaction_id)
    job = job_pb2.Job(company_public_key=company_public_key,
                      candidate_public_key=candidate_public_key,
                      job_id=job_id,
                      start=start)

    state.create_job_begin(job)


def job_end(state, public_key, transaction_id, payload):
    company = state.get_actor(public_key)
    _check_is_valid_actor(company)

    job_id = payload.data.job_id
    company_public_key = payload.data.company_public_key
    candidate_public_key = payload.data.candidate_public_key
    timestamp = payload.timestamp

    job = state.get_job(job_id, company_public_key, candidate_public_key)
    if not job:
        raise InvalidTransaction("Job doesn't exist")

    if public_key != candidate_public_key and public_key != company_public_key:
        raise InvalidTransaction("invalid end job actor")

    end = job_pb2.Job.End(timestamp=timestamp, transaction_id=transaction_id)
    state.update_job_end(job_id, company_public_key, candidate_public_key, end)
