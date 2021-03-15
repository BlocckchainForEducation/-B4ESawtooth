import json

from addressing.b4e_addressing import addresser
from config.config import SawtoothConfig
from protobuf.b4e_protobuf import payload_pb2
from rest_api.b4e_rest_api.transaction_creation.transaction_creation import _make_batch, _make_batch_multi_transactions, \
    slice_per


def make_create_actor(transaction_signer,
                      batch_signer,
                      profile,
                      timestamp):
    actor_address = addresser.get_actor_address(transaction_signer.get_public_key().as_hex())

    inputs = [actor_address]

    outputs = [actor_address]

    action = payload_pb2.CreateActorAction(data=json.dumps(profile), id=profile.get('uid'))

    payload = payload_pb2.B4EPayload(
        action=payload_pb2.B4EPayload.CREATE_ACTOR,
        create_institution=action,
        timestamp=timestamp)

    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer)


def make_create_institution(transaction_signer,
                            batch_signer,
                            profile,
                            timestamp):
    actor_address = addresser.get_actor_address(transaction_signer.get_public_key().as_hex())
    voting_address = addresser.get_voting_address(transaction_signer.get_public_key().as_hex())

    inputs = [actor_address, voting_address]

    outputs = [actor_address, voting_address]

    action = payload_pb2.CreateActorAction(data=json.dumps(profile), id=profile.get('universityName'))

    payload = payload_pb2.B4EPayload(
        action=payload_pb2.B4EPayload.CREATE_INSTITUTION,
        create_institution=action,
        timestamp=timestamp)

    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer)


def make_create_teacher(transaction_signer,
                        batch_signer,
                        profile,
                        timestamp):
    institution_address = addresser.get_actor_address(transaction_signer.get_public_key().as_hex())
    teacher_address = addresser.get_actor_address(profile['publicKey'])

    inputs = [institution_address, teacher_address]

    outputs = [teacher_address]

    action = payload_pb2.CreateTeacherAction(data=json.dumps(profile), teacher_public_key=profile['publicKey'],
                                             id=profile['teacherId'])

    payload = payload_pb2.B4EPayload(
        action=payload_pb2.B4EPayload.CREATE_TEACHER,
        create_teacher=action,
        timestamp=timestamp)

    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer)


def make_create_teachers(transaction_signer,
                         batch_signer,
                         profiles,
                         timestamp):
    institution_address = addresser.get_actor_address(transaction_signer.get_public_key().as_hex())

    list_profiles = slice_per(profiles, SawtoothConfig.MAX_BATCH_SIZE)
    list_batches = []
    for profiles in list_profiles:
        list_inputs = []
        list_outputs = []
        list_payload_bytes = []
        for profile in profiles:
            teacher_address = addresser.get_actor_address(profile['publicKey'])
            inputs = [institution_address, teacher_address]

            outputs = [teacher_address]

            action = payload_pb2.CreateTeacherAction(data=json.dumps(profile),
                                                     teacher_public_key=profile.get('publicKey'),
                                                     id=profile.get('teacherId'))

            payload = payload_pb2.B4EPayload(
                action=payload_pb2.B4EPayload.CREATE_TEACHER,
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


def make_update_profile(transaction_signer,
                        batch_signer,
                        profile,
                        timestamp):
    actor_address = addresser.get_actor_address(transaction_signer.get_public_key().as_hex())

    inputs = [actor_address]

    outputs = [actor_address]

    action = payload_pb2.UpdateActorProfileAction(data=json.dumps(profile))

    payload = payload_pb2.B4EPayload(
        action=payload_pb2.B4EPayload.UPDATE_ACTOR_INFO,
        update_actor_profile=action,
        timestamp=timestamp)

    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer)


def make_reject_institution(transaction_signer,
                            batch_signer,
                            institution_public_key,
                            timestamp):
    actor_address = addresser.get_actor_address(transaction_signer.get_public_key().as_hex())

    inputs = [actor_address]

    outputs = [actor_address]

    action = payload_pb2.RejectInstitutionAction(institution_public_key=institution_public_key)

    payload = payload_pb2.B4EPayload(
        action=payload_pb2.B4EPayload.REJECT_INSTITUTION,
        reject_institution=action,
        timestamp=timestamp)

    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer)


def make_active_institution(transaction_signer,
                            batch_signer,
                            institution_public_key,
                            timestamp):
    actor_address = addresser.get_actor_address(transaction_signer.get_public_key().as_hex())

    inputs = [actor_address]

    outputs = [actor_address]

    action = payload_pb2.RejectInstitutionAction(institution_public_key=institution_public_key)

    payload = payload_pb2.B4EPayload(
        action=payload_pb2.B4EPayload.ACTIVE_INSTITUTION,
        active_institution=action,
        timestamp=timestamp)

    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer)
