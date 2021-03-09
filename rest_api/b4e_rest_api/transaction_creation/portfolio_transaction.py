import json

from addressing.b4e_addressing import addresser
from config.config import SawtoothConfig
from protobuf.b4e_protobuf import payload_pb2
from rest_api.b4e_rest_api.transaction_creation.transaction_creation import slice_per, _make_batch, \
    _make_batch_multi_transactions


def make_create_edu_program(transaction_signer,
                            batch_signer,
                            student_public_key,
                            edu_program,
                            timestamp):
    institution_public_key = transaction_signer.get_public_key().as_hex()
    institution_address = addresser.get_actor_address(institution_public_key)
    edu_id = edu_program.get["eduProgramId"]
    portfolio_address = addresser.get_portfolio_address(edu_id, student_public_key,
                                                        institution_public_key)

    inputs = [institution_address, portfolio_address]

    outputs = [portfolio_address]

    action = payload_pb2.CreatePortfolioAction(id=edu_id,
                                               owner_public_key=student_public_key,
                                               portfolio_type=payload_pb2.EDU_PROGRAM,
                                               data=json.dumps(edu_program))

    payload = payload_pb2.B4EPayload(
        action=payload_pb2.B4EPayload.CREATE_EDU_PROGRAM,
        create_teacher=action,
        timestamp=timestamp)

    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer)


def make_create_edu_programs(transaction_signer,
                             batch_signer,
                             profiles,
                             timestamp):
    institution_public_key = transaction_signer.get_public_key().as_hex()
    institution_address = addresser.get_actor_address(institution_public_key)

    list_profiles = slice_per(profiles, SawtoothConfig.MAX_BATCH_SIZE)
    list_batches = []
    for profiles in list_profiles:
        list_inputs = []
        list_outputs = []
        list_payload_bytes = []
        for profile in profiles:
            edu_id = profile.get("eduProgramId")
            student_public_key = profile.get('publicKey')
            edu_program = profile
            edu_program_address = addresser.get_portfolio_address(edu_id,
                                                                  student_public_key,
                                                                  institution_public_key)
            inputs = [institution_address, edu_program_address]

            outputs = [edu_program_address]

            action = payload_pb2.CreatePortfolioAction(id=edu_id,
                                                       owner_public_key=student_public_key,
                                                       portfolio_type=payload_pb2.EDU_PROGRAM,
                                                       data=json.dumps(edu_program))

            payload = payload_pb2.B4EPayload(
                action=payload_pb2.B4EPayload.CREATE_EDU_PROGRAM,
                create_teacher=action,
                timestamp=timestamp)
            payload_bytes = payload.SerializeToString()

            list_inputs.append(inputs)
            list_outputs.append(outputs)
            list_payload_bytes.append(payload_bytes)

        batch = _make_batch_multi_transactions(
            list_payload_bytes=list_payload_bytes,
            list_inputs=list_inputs,
            list_outputs=list_outputs,
            transaction_signer=transaction_signer,
            batch_signer=batch_signer)
        list_batches.append(batch)

    return list_batches
