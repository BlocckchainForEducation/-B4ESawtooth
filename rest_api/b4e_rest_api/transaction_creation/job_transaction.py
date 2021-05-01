from addressing.b4e_addressing import addresser
from config.config import SawtoothConfig
from protobuf.b4e_protobuf import payload_pb2
from rest_api.b4e_rest_api.transaction_creation.transaction_creation import _make_batch, _make_batch_multi_transactions, \
    slice_per


def make_create_job(transaction_signer,
                    batch_signer,
                    company_public_key,
                    candidate_public_key,
                    job_id,
                    cipher,
                    record_hash,
                    timestamp):
    issuer_public_key = transaction_signer.get_public_key().as_hex()
    candidate_address = addresser.get_actor_address(candidate_public_key)
    company_address = addresser.get_actor_address(issuer_public_key)
    job_address = addresser.get_job_address(job_id, company_public_key, candidate_public_key)

    inputs = [candidate_address, company_address, job_address]

    outputs = [job_address]

    action = payload_pb2.JobBeginAction(company_public_key=company_public_key,
                                        candidate_public_key=candidate_public_key,
                                        record_id=job_id,
                                        cipher=cipher,
                                        hash=record_hash)

    payload = payload_pb2.B4EPayload(
        action=payload_pb2.B4EPayload.JOB_BEGIN,
        create_record=action,
        timestamp=timestamp)

    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer)


def make_update_job_end(transaction_signer,
                        batch_signer,
                        company_public_key,
                        candidate_public_key,
                        job_id,
                        timestamp):
    issuer_public_key = transaction_signer.get_public_key().as_hex()
    candidate_address = addresser.get_actor_address(candidate_public_key)
    company_address = addresser.get_actor_address(issuer_public_key)
    job_address = addresser.get_job_address(job_id, company_public_key, candidate_public_key)

    inputs = [candidate_address, company_address, job_address]

    outputs = [job_address]

    action = payload_pb2.JobEndAction(company_public_key=company_public_key,
                                      candidate_public_key=candidate_public_key,
                                      record_id=job_id, )

    payload = payload_pb2.B4EPayload(
        action=payload_pb2.B4EPayload.JOB_END,
        create_record=action,
        timestamp=timestamp)

    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer)
